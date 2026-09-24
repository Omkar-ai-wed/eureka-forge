'''
Manim Show Me Why selector and metadata service (Prompt 06).
Deterministic frontend selection from concept/misconception context.
'''
from __future__ import annotations
from typing import Any
from ..schemas.models import ManimClipMetadata, MisconceptionRule

CLIPS: dict[str, ManimClipMetadata] = {
    'clip_superposition': ManimClipMetadata(
        clip_id='clip_superposition',
        title='H Gate -> Superposition: Rotation to the Equatorial Plane',
        concept='superposition',
        description='Visualizes the qubit state vector on the Bloch sphere being rotated by the Hadamard operator from |0> to the balanced superposition state (|0> + |1>)/sqrt(2).',
        duration_sec=14.5,
        video_url='/videos/manim_superposition.mp4',
        misconception_ids=['M1'],
        key_takeaways=[
            'The Hadamard gate rotates the state vector from the North Pole (|0>) directly onto the equator (|+>).',
            'Superposition is not a random hidden coin; it is a coherent quantum amplitude distribution.',
            'Measurement forces projection: 50% probability of |0>, 50% probability of |1>.'
        ],
        fallback_explanation=(
            'Bloch Sphere Transformation: Vector initially points at North Pole (Z = +1, State |0>). '
            'Applying Hadamard rotates the vector 90 degrees onto the X-axis (State |+> = (|0> + |1>)/sqrt(2)). '
            'Equal distance to North and South poles produces equal 50% measurement probabilities.'
        )
    ),
    'clip_measurement': ManimClipMetadata(
        clip_id='clip_measurement',
        title='Measurement -> Wavefunction Collapse & State Update',
        concept='measurement',
        description='Demonstrates how measurement actively interacts with a quantum state, projecting a superposition into a definitive basis state.',
        duration_sec=12.0,
        video_url='/videos/manim_measurement.mp4',
        misconception_ids=['M2'],
        key_takeaways=[
            'Measurement is an active projection operator, not a passive camera snapshot.',
            'Upon measurement, the state collapses irreversibly to the observed basis state (|0> or |1>).',
            'Immediate subsequent measurements will return the exact same outcome with 100% certainty.'
        ],
        fallback_explanation=(
            'Wavefunction Collapse: When a superposition state is measured, '
            'the quantum state instantly updates to either |0> (with probability |alpha|^2) or |1> (with probability |beta|^2). '
            'The original superposition is permanently destroyed.'
        )
    ),
    'clip_bell': ManimClipMetadata(
        clip_id='clip_bell',
        title='H + CNOT -> Bell State Entanglement',
        concept='entanglement',
        description='Shows two independent qubits becoming non-separable through H followed by CNOT, producing the maximally entangled Bell state Phi+.',
        duration_sec=16.0,
        video_url='/videos/manim_bell.mp4',
        misconception_ids=['M3'],
        key_takeaways=[
            'The composite state cannot be factored into individual qubit states: |Phi+> = (|00> + |11>)/sqrt(2).',
            'Outcomes are perfectly correlated (|00> and |11>) without any signal transmitted between qubits.',
            'States |01> and |10> have zero probability.'
        ],
        fallback_explanation=(
            'Entanglement Generation: Qubit 0 is placed in superposition (|0> + |1>)/sqrt(2). '
            'CNOT uses qubit 0 as control and qubit 1 as target. When control is |0>, target remains |0> (|00>). '
            'When control is |1>, target flips to |1> (|11>). The resulting quantum state is entangled: '
            'measuring qubit 0 instantaneously determines qubit 1, with zero possibility of mismatched states.'
        )
    )
}

def list_clips() -> list[ManimClipMetadata]:
    return list(CLIPS.values())

def get_clip(clip_id: str) -> ManimClipMetadata | None:
    return CLIPS.get(clip_id)

def select_clip_for_context(concept: str | None = None, rule: MisconceptionRule | None = None) -> ManimClipMetadata:
    if rule == MisconceptionRule.M1 or (concept and 'superposition' in concept.lower()):
        return CLIPS['clip_superposition']
    elif rule == MisconceptionRule.M2 or (concept and 'measurement' in concept.lower()):
        return CLIPS['clip_measurement']
    elif rule == MisconceptionRule.M3 or (concept and ('entanglement' in concept.lower() or 'bell' in concept.lower())):
        return CLIPS['clip_bell']
    return CLIPS['clip_superposition']
