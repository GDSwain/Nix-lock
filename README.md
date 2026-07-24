# Nix-Lock

*A delayed deployment workflow for NixOS.*

## What is Nix-Lock?

Most update workflows answer the question:

> **“What is the latest version available?”**

Nix-Lock answers a different question:

> **“Which previously captured operating system has completed its observation period?”**

Rather than immediately deploying every newly built NixOS system, Nix-Lock separates the act of building a system from the act of deploying it.

A candidate system is built once, preserved unchanged, observed for a configurable period, and intentionally deployed later.

The result is a release management workflow that separates **candidate capture** from **deployment** while preserving the normal NixOS administration experience.

## Why?

New software releases occasionally introduce regressions, incompatibilities, or unexpected behaviour.

Many users respond by waiting before updating. However, waiting manually usually means installing whatever revision happens to be current when the waiting period ends.

That is not the same as allowing one specific revision to complete an observation period.

Nix-Lock solves this by building and preserving an exact immutable NixOS system closure at a chosen point in time.

That same closure can then be deployed later, regardless of how the available configuration or package sources have changed in the meantime.

The goal is not to avoid updates.

The goal is to make deployment intentional.

## How It Works

The workflow is deliberately simple:

```text
Capture → Observe → Deploy → Repeat
```

1. Build the current NixOS configuration without activating it.
2. Preserve the resulting immutable system closure.
3. Continue using and maintaining the computer normally.
4. Allow the candidate to complete its observation period unchanged.
5. Deploy that exact candidate.
6. Capture the next candidate.

Personal files, documents, development work, and ordinary system use continue normally.

Only the timing of operating system deployment changes.

## Architecture

Nix-Lock does not maintain its own archive of operating systems.

Nix already stores immutable system closures and already provides the mechanisms required to protect and activate them.

Nix-Lock therefore owns one persistent garbage-collection root:

```text
~/.local/state/nix-lock/candidate
```

That root:

* identifies the retained candidate
* protects the candidate from garbage collection
* provides a stable location from which the candidate can be inspected

Nix continues to own storage, closure identity, activation, and garbage collection.

Nix-Lock adds policy around when an already-built closure should be deployed.

## Project Goals

Nix-Lock aims to:

* Build immutable NixOS deployment candidates.
* Preserve candidates unchanged.
* Separate build time from deployment time.
* Support configurable observation periods.
* Deploy previously built system closures.
* Preserve reproducibility.
* Integrate with existing NixOS workflows.
* Minimise operational complexity.

## Non-Goals

Nix-Lock is **not** intended to:

* Replace NixOS generations.
* Replace backups.
* Snapshot user data.
* Restore complete machine state.
* Predict whether updates are safe.
* Test packages.
* Replace Git.
* Replace existing NixOS tooling.
* Require Home Manager.
* Require users to redesign an existing NixOS configuration.

## Current Status

Nix-Lock has completed its first implementation milestone.

The current proof of concept can:

* build a NixOS system without activating it
* identify the resulting immutable system closure
* preserve that closure using a persistent garbage-collection root
* verify that the retained closure is a valid NixOS system
* report the currently retained candidate
* safely replace an earlier candidate

The project is now in an intentional observation phase.

A candidate has been captured and preserved while the computer continues through ordinary daily use and future system rebuilds.

The next milestone is to demonstrate that the retained candidate remains available and deployable after the observation period.

For that reason, a period of limited repository activity is expected and does not indicate that the project has been abandoned.

The current experiment requires time to pass.

## Development Approach

Nix-Lock is being developed experimentally.

Assumptions are tested before additional abstraction or automation is introduced.

Failed approaches are documented rather than removed from the project history because they explain how the current design was reached and may help others avoid repeating the same investigation.

The project should remain as small as its purpose allows.

Where Nix already provides the required mechanism, Nix-Lock should use it rather than replace it.

## Documentation

The project documentation records:

* the original problem
* rejected approaches
* experimental findings
* architectural decisions
* current implementation
* remaining milestones

It is the authoritative description of the project's intended behaviour and the reasoning behind its design.

## Contributing

Ideas, experiments, corrections, and constructive feedback are welcome.

Alternative approaches are particularly useful when they are accompanied by an explanation of what was tested and what was observed.

The project deliberately favours simplicity over features.

Proposed changes should support the central aim of separating system capture from system deployment without unnecessarily increasing operational complexity.

## License

This project is released under the MIT License.

-- Oggie --
