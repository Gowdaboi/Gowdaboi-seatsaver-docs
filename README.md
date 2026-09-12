# Seat Saver

Seating and service management for catered events — built for Indian
wedding-style functions, where guests are seated and served in timed rounds
rather than all at once.

## The problem

At a large function, seating is run on paper and by shouting. A floor manager
holds the layout in their head, guests mill around waiting to be told where to
sit, and when a table is served and cleared nobody quite knows which seats are
free for the next sitting. The failure mode isn't dramatic — it's a constant
low-grade friction that gets worse as the hall gets bigger, and it lands on
whoever is least able to fix it mid-service.

**Pankti** (banana-leaf) service makes this sharper. Guests eat in *rounds*:
one sitting is served, cleared, and the next group takes those same seats. A
seat isn't simply free or taken — it's free *for a particular round*, which is
the thing a paper chart cannot express.

## What it does

**For the caterer**

- Design the floor once — sections, tables and seats, laid out as a plan
  rather than drawn to scale
- Run dining rounds: start a sitting, see who is seated, hand seats to the
  next round as they clear
- Assign walk-ins and VIPs directly, without the guest needing an account
- Scan a guest's QR at the door to check them in
- Handle no-shows: seats held past their timeout are released and offered on
  to waiting guests in order
- Keep a recap of every past event — floor, menu and bookings

**For the guest**

- Scan a QR code at the venue; no app install, no account signup
- See the menu and the actual floor plan the host designed
- Book a seat for the next round with room
- Get an SMS reminder before the round starts, with a one-tap link to cancel
  and free the seat for someone else

## Tech

- **Flutter** — one codebase, running on web and Android
- **Supabase** — Postgres with Row Level Security, Auth, Realtime, and Edge
  Functions
- **Twilio** — SMS and WhatsApp for guest verification and round reminders

Multi-tenancy is enforced in the database rather than the application: every
caterer's data is isolated by row-level policies, so an app-layer bug cannot
leak one caterer's event into another's. Anything that has to be atomic, or
that legitimately needs to read across that boundary, runs as a database
function that begins by checking who is asking.

## A few design decisions worth explaining

**Seat availability is derived, never stored.** There is no table recording
"seat 4 is taken for round 2". A seat is taken for a round if an active
booking for that round holds it — and that is computed on read. The stored
version would have been faster and would have started lying the first time a
booking was cancelled by one path and not another.

**The host's floor designer and the guest's seat picker are the same
renderer.** Not two views of shared data — literally one component. What the
host arranges is what the guest books from, so the two cannot drift apart as
either side changes.

**Events are archived, never deleted.** A caterer running two functions a week
accumulates a hundred a year, and they clutter every picker in the app.
Archiving hides an event completely while preserving the floor, menu, bookings
and recap. The only thing that truly deletes is a host deleting their whole
account, which is a different intent entirely.

**A missed reminder stays missed.** Round reminders count back from a round's
*scheduled* start, not the moment the host presses Start — which is too late
to warn anyone. If the send window is missed, nothing is sent: a late "starts
in 5 minutes" is worse than silence.

**Cancelling a booking frees only the seats it is actually holding.** A
booking for a later sitting holds no physical seat yet, so releasing
everything it points at would evict whoever is sitting there right now.

## Current state

Working and deployed on the web. The Android build is signed and preparing for
Play Store release. The guest booking flow, host floor design, dining rounds,
QR check-in, no-show handling and reminder delivery are all implemented
against live data.

SMS delivery currently runs on a Twilio trial account, which only reaches
pre-verified numbers — production messaging in India additionally requires DLT
template registration.

## Privacy and data deletion

See [privacy-policy.html](privacy-policy.html).

Hosts can permanently delete their account and all associated data from inside
the app, or request deletion by email — see
[Delete your account](https://gowdaboi.github.io/Gowdaboi-seatsaver-docs/delete-account.html).

## Try it

The web app runs at
[gowdaboi.github.io/Gowdaboi-seatsaver-docs](https://gowdaboi.github.io/Gowdaboi-seatsaver-docs/).

## About this repository

This repo holds the public face of Seat Saver: this overview, the privacy
policy and account-deletion page, and the compiled web build that serves the
app. **The source is not here** — the Flutter and database code, the schema and
row-level security policies, and the design decision log all live in a separate
private repository. What you can see here is what any visitor's browser
downloads to run the app.
