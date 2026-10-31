# Nix-Lock

*A delayed deployment experiment for NixOS.*

**Project status: Discontinued — experimental proof of concept.**

## What is Nix-Lock?

Nix-Lock was developed to investigate whether NixOS system updates could be built, preserved, and deployed after a defined observation period.

Rather than immediately activating a newly built operating system, Nix-Lock separated the process into three stages:

```text
Capture → Observe → Deploy
```

The intention was to introduce a delay between building and deploying updates while allowing ordinary system administration to continue.

The project successfully demonstrated the underlying mechanism. However, subsequent evaluation established that the resulting behaviour did not satisfy the original requirements.

**Development has ended, and Nix-Lock is retained as a documented engineering experiment.**

## Motivation

Software updates occasionally introduce regressions, incompatibilities, or unexpected behaviour.

One approach to reducing this risk is to delay deployment until a particular software revision has completed an observation period.

Simply waiting before updating is insufficient because the available software may change during that period.

Nix-Lock attempted to address this by capturing an exact immutable NixOS system closure, preserving it unchanged, and deploying that same closure later.

The objective was to make deployment deliberate without unnecessarily complicating normal NixOS administration.

## How It Works

The experimental workflow consisted of:

1. Building the current NixOS configuration without activating it.
2. Identifying the resulting immutable system closure.
3. Preserving that closure using a persistent garbage-collection root.
4. Continuing normal system use and maintenance.
5. Allowing an observation period to pass.
6. Activating the previously captured closure.
7. Verifying that the intended closure became the running system.

The observation period was determined by the user rather than enforced by Nix-Lock.

## Usage

Enter the development environment:

```bash
nix-shell
```

The proof-of-concept interface provides three commands:

```text
python3 nix_lock.py {capture|status|deploy}
```

### Capture

```bash
python3 nix_lock.py capture
```

Builds the current NixOS configuration without activating it.

The resulting system closure is validated and retained using a persistent garbage-collection root.

When replacing an existing candidate, Nix-Lock protects the new closure before releasing its reference to the previous candidate.

### Status

```bash
python3 nix_lock.py status
```

Reports the retained candidate and verifies that:

- The store path exists.
- Garbage-collection protection is present.
- The candidate contains a valid NixOS system activation program.

### Deploy

```bash
python3 nix_lock.py deploy
```

Activates the exact previously captured system closure.

The command does not rebuild the current configuration or reconstruct the candidate from current package sources.

After activation, Nix-Lock verifies that `/run/current-system` resolves to the retained candidate.

**These commands are preserved for historical and educational purposes. Nix-Lock is not recommended as a production deployment workflow.**

## Architecture

Nix-Lock deliberately avoided implementing its own operating system archive.

Nix already provides immutable system closures, stable store paths, garbage collection, and system activation mechanisms.

Nix-Lock used a persistent garbage-collection root:

```text
~/.local/state/nix-lock/candidate
```

This root served three purposes:

- Identifying the retained candidate.
- Protecting the candidate from garbage collection.
- Providing a stable reference for inspection and deployment.

The implementation relied on existing NixOS functionality wherever possible.

This approach kept the proof of concept relatively small and avoided unnecessary duplication of established mechanisms.

## Original Project Goals

Nix-Lock was intended to:

- Build immutable NixOS deployment candidates.
- Preserve candidates unchanged during an observation period.
- Separate build time from deployment time.
- Deploy previously built system closures.
- Preserve reproducibility.
- Allow normal system maintenance to continue.
- Integrate with existing NixOS administration workflows.
- Minimise additional operational complexity.

The final two objectives proved particularly important when evaluating the project's success.

## Non-Goals

Nix-Lock was not intended to:

- Replace NixOS generations.
- Replace backups.
- Snapshot user data.
- Restore complete machine state.
- Predict whether updates were safe.
- Test individual packages.
- Replace Git.
- Replace existing NixOS tooling.
- Require Home Manager.

## Experimental Validation

The first complete operational experiment began on August 1, 2026.

A NixOS system closure was captured and protected using a persistent garbage-collection root.

The candidate remained unchanged while the computer continued through almost four weeks of ordinary use, configuration changes, rebuilds, and maintenance.

At the end of the observation period, Nix-Lock confirmed:

```text
Store path: present
GC protection: present
NixOS system closure: valid
```

The retained candidate was subsequently activated without rebuilding it.

Independent verification using:

```bash
readlink -f /run/current-system
```

confirmed that the running system matched the closure captured almost four weeks earlier.

The experiment demonstrated that:

- NixOS system closures can be built without activation.
- Immutable closures can be preserved independently of subsequent configuration changes.
- Retained closures can survive extended observation periods.
- Previously built closures can be activated without rebuilding.
- The activated system can be verified against the retained candidate.

The central technical hypothesis was therefore demonstrated successfully.

## Final Evaluation

Although the capture, retention, and deployment mechanisms worked, operational evaluation exposed a fundamental limitation.

A previously captured NixOS closure represents an entire operating system configuration at a particular point in time.

Activating that closure does not selectively introduce delayed updates into the currently configured system.

Instead, it activates the earlier system configuration, potentially reversing system-level changes made during the observation period.

This behaviour conflicted with the intended workflow.

The original objective was to delay deployment of selected system changes while preserving the normal evolution of the machine.

Nix-Lock could preserve and activate an earlier system closure, but it could not reconcile that closure with configuration changes introduced after capture.

Consequently, the workflow offered insufficient practical advantage over NixOS's existing generation management and rollback mechanisms.

The implementation achieved its immediate technical objectives but failed to deliver the intended operational benefits.

## Project Conclusion

**Nix-Lock did not meet its criteria for success.**

The project successfully demonstrated that immutable NixOS system closures could be captured, preserved, and deployed at a later date.

However, the resulting workflow introduced undesirable consequences and did not satisfy the original requirement to preserve ongoing system evolution while deploying delayed updates.

Further development would have required reconsidering the fundamental approach rather than simply extending the existing implementation.

Development was therefore discontinued.

Nix-Lock remains publicly available as an engineering experiment documenting its original hypothesis, implementation, testing, findings, and eventual retirement.

The project illustrates an important distinction between demonstrating that a mechanism works and establishing that the mechanism provides a useful solution.

## Documentation

The accompanying `nix-lock.org` document preserves the detailed development record, including:

- The original problem and design objectives.
- Early hypotheses and rejected approaches.
- Investigation of NixOS system closures.
- Architectural decisions.
- Implementation details.
- Experimental observations.
- The first complete deployment cycle.
- The reasoning behind the project's conclusion.

Some sections reflect the project's status during active development and are retained as historical documentation.

## License

This project is released under the MIT License.

---

*Oggie*
