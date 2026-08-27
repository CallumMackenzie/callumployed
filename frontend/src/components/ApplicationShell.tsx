import shellDocument from "../../../src/callumployed/web/static/shell.html?raw";

const parsedShell = new DOMParser().parseFromString(shellDocument, "text/html");
const shellMarkup = parsedShell.body.innerHTML;

export function ApplicationShell() {
  return (
    <div
      className="react-application"
      dangerouslySetInnerHTML={{ __html: shellMarkup }}
    />
  );
}
