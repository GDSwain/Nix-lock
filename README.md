# Nix-Lock

*A delayed deployment workflow for NixOS.*

## What is Nix-Lock?

Most update workflows answer the question:

> **"What is the latest version available?"**

Nix-Lock answers a different question:

> **"Which previously captured version has had sufficient time to prove itself?"**

Rather than deploying the latest available NixOS revision immediately, Nix-Lock captures an immutable revision, preserves it for a configurable observation period, and intentionally deploys that exact revision later.

The result is a deployment workflow that separates **revision capture** from **deployment**, while preserving the normal NixOS user experience.

## Why?

New software releases occasionally introduce regressions, incompatibilities, or unexpected behaviour.

Many users choose to "wait a while before updating", but doing so manually usually means installing whatever happens to be current when they eventually update—not the version they originally intended to use.

Nix-Lock solves this by capturing a specific NixOS revision at a chosen point in time and deploying *that exact revision* after an observation period.

The goal is not to avoid updates.

The goal is to make deployment intentional.

## How it Works

The workflow is deliberately simple:

```
Capture → Observe → Deploy → Repeat
```

1. Capture today's NixOS revision.
2. Continue using the system normally.
3. Allow the captured revision to mature under real-world use.
4. Deploy that exact revision.
5. Capture the next candidate.

Personal files, documents, and day-to-day usage continue as normal. Only the timing of system deployment changes.

## Project Goals

Nix-Lock aims to:

* Capture immutable NixOS revisions.
* Delay deployment by a configurable observation period.
* Preserve reproducibility.
* Integrate with existing NixOS workflows.
* Minimise operational complexity.

## Non-Goals

Nix-Lock is **not** intended to:

* Replace NixOS generations.
* Replace backups.
* Snapshot user data.
* Predict whether updates are safe.
* Test packages.
* Replace existing NixOS tooling.
* Require users to redesign an existing NixOS configuration.

## Current Status

Nix-Lock is currently in the design and proof-of-concept stage.

The project's primary focus is validating the deployment workflow before introducing automation.

## Documentation

The project documentation describes the design goals, guiding principles, terminology, and reasoning behind Nix-Lock.

As the project evolves, the documentation will remain the authoritative description of its intended behaviour.

## Contributing

Ideas, discussion, and constructive feedback are welcome.

The project deliberately favours simplicity over features. Any proposed changes should support the project's central aim of separating revision capture from deployment without unnecessarily increasing complexity.

## License

This project is released under the MIT License.

