from dataclasses import dataclass

import turso

from callumployed.central.client import CentralStoreClient, CentralStoreError
from callumployed.central.models import CentralRole, ResolveCompanyRequest
from callumployed.data.models import Company, CompanyCareerPage, Role
from callumployed.data.repositories import (
    add_company,
    add_company_career_page,
    list_companies,
    list_companies_without_central_id,
    list_company_career_pages,
    set_company_central_link,
    set_company_central_sync_status,
    upsert_central_role,
)


@dataclass(frozen=True)
class ResolveCompaniesResult:
    linked: int = 0
    created: int = 0
    needs_review: int = 0
    failed: int = 0


@dataclass(frozen=True)
class PullRolesResult:
    companies_created: int = 0
    roles_created: int = 0
    roles_updated: int = 0
    skipped_roles: int = 0


def resolve_unlinked_companies(
    connection: turso.Connection,
    client: CentralStoreClient,
) -> ResolveCompaniesResult:
    result = ResolveCompaniesResult()
    for company in list_companies_without_central_id(connection):
        if company.id is None:
            continue
        try:
            response = client.resolve_company(
                ResolveCompanyRequest(
                    name=company.name,
                    career_page_urls=[
                        career_page.url
                        for career_page in list_company_career_pages(connection, company.id)
                    ],
                )
            )
        except CentralStoreError as error:
            set_company_central_sync_status(
                connection,
                company.id,
                status="failed",
                error=str(error),
            )
            result = ResolveCompaniesResult(
                linked=result.linked,
                created=result.created,
                needs_review=result.needs_review,
                failed=result.failed + 1,
            )
            continue

        if response.action == "needs_review" or response.global_company_id is None:
            set_company_central_sync_status(connection, company.id, status="needs_review")
            result = ResolveCompaniesResult(
                linked=result.linked,
                created=result.created,
                needs_review=result.needs_review + 1,
                failed=result.failed,
            )
            continue

        set_company_central_link(
            connection,
            company.id,
            central_company_id=response.global_company_id,
            canonical_domain=response.canonical_domain,
            normalized_name=response.normalized_name,
        )
        result = ResolveCompaniesResult(
            linked=result.linked + int(response.action == "matched"),
            created=result.created + int(response.action == "created"),
            needs_review=result.needs_review,
            failed=result.failed,
        )
    return result


def pull_roles(
    connection: turso.Connection,
    client: CentralStoreClient,
) -> PullRolesResult:
    central_roles = client.list_roles().roles
    local_companies_by_central_id = {
        company.central_company_id: company
        for company in list_companies(connection, include_inactive=True)
        if company.central_company_id is not None
    }
    result = PullRolesResult()

    for central_role in central_roles:
        company = local_companies_by_central_id.get(central_role.global_company_id)
        company_created = False
        if company is None:
            company = _create_company_from_central_role(connection, central_role)
            local_companies_by_central_id[central_role.global_company_id] = company
            company_created = True
        if company.id is None:
            result = PullRolesResult(
                companies_created=result.companies_created + int(company_created),
                roles_created=result.roles_created,
                roles_updated=result.roles_updated,
                skipped_roles=result.skipped_roles + 1,
            )
            continue

        role, created = upsert_central_role(
            connection,
            Role(
                company_id=company.id,
                title=central_role.title,
                role_url=central_role.role_url,
                location=central_role.location,
                description=central_role.description,
                posting_id=central_role.posting_id,
                central_role_id=central_role.global_role_id,
                central_source="central",
            ),
        )
        _ = role
        result = PullRolesResult(
            companies_created=result.companies_created + int(company_created),
            roles_created=result.roles_created + int(created),
            roles_updated=result.roles_updated + int(not created),
            skipped_roles=result.skipped_roles,
        )

    return result


def _create_company_from_central_role(
    connection: turso.Connection,
    central_role: CentralRole,
) -> Company:
    company = add_company(
        connection,
        Company(
            name=central_role.company_name,
            prestige_tier=central_role.tier_classification,
            central_company_id=central_role.global_company_id,
            central_sync_status="linked",
        ),
    )
    if company.id is not None:
        add_company_career_page(
            connection,
            CompanyCareerPage(company_id=company.id, url=central_role.role_url, label="Central"),
        )
    return company

