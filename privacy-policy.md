# Privacy Policy — Seat Saver

**Last updated:** 12/9/26

Seat Saver ("the app") is operated by AnyProblem Apps. This policy explains what information the app collects, why, and how it is handled.

## Who this applies to

Seat Saver has two kinds of users:

- **Hosts** — caterers or floor managers who create and run events in the app.
- **Guests** — attendees at those events, who use the app to book a seat and check in.

## Information we collect

**From hosts:** email address and business name, used to create and secure your account (Supabase Auth, email/password).

**From guests:** phone number and name, used to verify your identity via SMS one-time password (OTP) and to prevent duplicate bookings at the same event. We do not require a guest to create a password or provide an email.

**Event and booking data:** seat selections, booking timestamps, no-show/arrival status, and any feedback a guest submits to a host. This data is scoped to the specific event and is visible only to that event's host and to the guest who made the booking.

**Camera access:** the app requests camera permission to scan QR codes (for event check-in and booking confirmation). The camera feed is processed on your device to read the QR code and is not recorded, stored, or transmitted as an image or video.

**We do not collect:** precise location data, contacts, photos/media beyond the QR scan above, or advertising identifiers. We do not show ads.

## How information is used

- To authenticate hosts and guests and keep each caterer's event data isolated from every other caterer (multi-tenant data separation, enforced at the database level).
- To manage seating, dining rounds, and no-show/reassignment logic during an event.
- To send booking confirmations and round-start reminders by SMS (via Twilio) to the phone number a guest provides.
- To send account-related email (e.g. confirmation, password reset) to hosts via Supabase's email service.

## How information is stored and protected

Data is stored in a Supabase-hosted Postgres database with Row Level Security enabled, meaning each caterer's data (and each guest's own booking data) is enforced as accessible only to that caterer or that guest at the database level — not just in the app's interface.

## Third-party services

- **Supabase** (database, authentication, realtime updates) — https://supabase.com/privacy
- **Twilio** (SMS delivery for guest OTP and reminders) — https://www.twilio.com/en-us/legal/privacy

These providers process data on our behalf under their own privacy and security terms.

## Data retention and deletion

Event and booking data is retained for as long as the host's account exists, because the app's past-event records are the reason a caterer keeps using it — there is no fixed expiry after which an event is discarded.

Deletion is under the host's control and is immediate:

- **In the app:** Host dashboard → Account → Delete account.
- **If you have uninstalled it:** see https://gowdaboi.github.io/Seat-saver/delete-account.html

Deleting a host account permanently removes that account, every event it owns, and all data scoped to those events — floor layouts, menus, rounds, and all guest bookings including seat history and the phone numbers guests provided. This is a deletion, not a deactivation: the records are removed from the database and cannot be restored afterwards, by you or by us.

Guest records are shared between caterers, since a guest is identified by their own phone number. If you booked with more than one caterer, one of them deleting their account removes all of their events' data about you, while your records with the other caterer remain. A guest who booked with only that caterer is removed completely, phone number included.

**Guests:** to have your own phone number and booking history removed, email kushaldayanand243@gmail.com from the account it is registered to, or include the phone number you booked with so it can be matched. Requests are actioned within 30 days, usually within a few working days.

## Children's privacy

Seat Saver is intended for use by adults managing or attending catered events and is not directed at children.

## Changes to this policy

We may update this policy as the app changes. The "Last updated" date above will reflect the most recent revision.

## Contact

Questions about this policy or your data can be sent to kushaldayanand243@gmail.com.
