# Security

Busview reads firmware tables, device descriptors and drive logs, which are untrusted input, and it can run with administrator rights. A flaw in how it parses them matters.

## Reporting a vulnerability

Report it privately through GitHub: open the repository's **Security** tab and choose **Report a vulnerability**. Please do not open a public issue for it.

Include what you can of:

- The Busview version, or the commit you built.
- What input or machine triggers it. A snapshot or report helps; exports hide serial numbers by default.
- What happens: a crash, a wrong reading presented as fact, or anything written or sent that should not be.

You will get a reply saying whether it is accepted and what happens next.

## What Busview promises

- It installs no kernel driver and reads everything from user mode.
- It changes nothing on the computer except the snapshot and report files you ask for.
- It sends nothing anywhere. The only network request it ever makes is the database update check, and only when you press Check for update.
- Crash reports are written beside the program and stay there.

A behaviour that breaks one of these is a security bug, whatever its cause.
