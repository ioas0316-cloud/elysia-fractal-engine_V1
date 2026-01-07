"""Reinforcement learning caretaker simulation for nurturing Elysia.

This module provides a lightweight virtual environment where a caretaker
can practice teaching and praising cycles similar to guiding a child. The
goal is to model phrases such as "철수는 바나나를 먹어요" and warm
reinforcement when words like "엄마" or "아빠" appear. A simple
Q-learning caretaker is included so we can iterate on training routines
without requiring real-time interaction.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import random


ConceptId = str
ActionName = str
State = Tuple[int, int, int]


@dataclass(frozen=True)
class StepLog:
    """Snapshot of a single caretaker→child exchange."""

    step_index: int
    action: ActionName
    reward: float
    child_output: str
    knowledge: Dict[ConceptId, float]
    success: bool
    concept: Optional[ConceptId]


@dataclass(frozen=True)
class EpisodeLog:
    """Record of one full caretaker training episode."""

    episode_index: int
    total_reward: float
    steps: List[StepLog]


class VirtualChildEnvironment:
    """Environment modelling a caregiver nurturing vocabulary and concepts.

    The caretaker can select structured actions such as introducing a
    sentence, prompting the child to recall it, or offering praise. The
    environment tracks concept mastery scores in ``[0, 1]`` and returns a
    shaped reward encouraging: (1) gentle teaching before testing, (2)
    praising only after successful attempts, and (3) balanced exposure to
    different family-oriented concepts.
    """

    ACTIONS: Tuple[ActionName, ...] = (
        "introduce_banana_story",
        "prompt_banana_sentence",
        "prompt_say_mom",
        "prompt_say_dad",
        "celebrate_success",
        "soothing_encouragement",
    )

    def __init__(
        self,
        seed: Optional[int] = None,
        mastery_threshold: float = 0.85,
        max_steps: int = 40,
    ) -> None:
        self.mastery_threshold = mastery_threshold
        self.max_steps = max_steps
        self._rng = random.Random(seed)
        self.knowledge: Dict[ConceptId, float] = {}
        self._step_count = 0
        self._last_success: bool = False
        self._last_concept: Optional[ConceptId] = None
        self._transcript: List[StepLog] = []
        self.reset()

    def reset(self) -> State:
        """Reset the child state and return the initial observation."""

        self.knowledge = {
            "banana_sentence": 0.05,
            "say_mom": 0.05,
            "say_dad": 0.05,
        }
        self._step_count = 0
        self._last_success = False
        self._last_concept = None
        self._transcript = []
        return self._observe()

    def _observe(self) -> State:
        bins = 5
        return tuple(
            min(bins - 1, int(level * bins))
            for level in (
                self.knowledge["banana_sentence"],
                self.knowledge["say_mom"],
                self.knowledge["say_dad"],
            )
        )

    def _clip(self, value: float) -> float:
        return max(0.0, min(1.0, value))

    def _log_step(
        self,
        step_index: int,
        action: ActionName,
        reward: float,
        child_output: str,
        success: bool,
        concept: Optional[ConceptId],
    ) -> None:
        self._transcript.append(
            StepLog(
                step_index=step_index,
                action=action,
                reward=reward,
                child_output=child_output,
                knowledge=dict(self.knowledge),
                success=success,
                concept=concept,
            )
        )

    def _prob_success(self, concept: ConceptId) -> float:
        base = self.knowledge[concept]
        return self._clip(base)

    def step(self, action: ActionName) -> Tuple[State, float, bool, Dict[str, object]]:
        """Advance one caretaker action and return observation, reward, done."""

        if action not in self.ACTIONS:
            raise ValueError(f"Unknown action: {action}")

        self._step_count += 1
        reward = -0.02  # gentle pressure to finish in fewer steps
        child_output = "아이: 조용히 숨을 고르고 있어요."
        success = False
        concept: Optional[ConceptId] = None

        if action == "introduce_banana_story":
            growth = 0.25 * (1.0 - self.knowledge["banana_sentence"])
            self.knowledge["banana_sentence"] = self._clip(
                self.knowledge["banana_sentence"] + growth
            )
            reward += 0.1 + growth
            self._last_success = False
            child_output = "아이: 조용히 듣고 있어요. 철수와 바나나 이야기를 떠올려요."
        elif action == "prompt_banana_sentence":
            concept = "banana_sentence"
            success_prob = self._prob_success(concept)
            success = self._rng.random() < success_prob
            if success:
                boost = 0.12 * (1.0 - self.knowledge[concept])
                self.knowledge[concept] = self._clip(self.knowledge[concept] + boost)
                reward += 1.0 + self.knowledge[concept]
                child_output = "아이: \"철수는 바나나를 먹어요!\" 라고 환하게 말해요."
                self._last_success = True
                self._last_concept = concept
            else:
                reward -= 0.25
                child_output = "아이: 아직 문장이 헷갈려요. 눈을 동그랗게 뜨고 있어요."
                self._last_success = False
        elif action == "prompt_say_mom":
            concept = "say_mom"
            success_prob = self._prob_success(concept)
            success = self._rng.random() < success_prob
            if success:
                boost = 0.1 * (1.0 - self.knowledge[concept])
                self.knowledge[concept] = self._clip(self.knowledge[concept] + boost)
                reward += 0.8 + self.knowledge[concept]
                child_output = "아이: 작은 목소리로 \"엄마\"라고 부르며 미소 짓습니다."
                self._last_success = True
                self._last_concept = concept
            else:
                reward -= 0.2
                child_output = "아이: 입술을 달싹이지만 아직 말이 나오지 않아요."
                self._last_success = False
        elif action == "prompt_say_dad":
            concept = "say_dad"
            success_prob = self._prob_success(concept)
            success = self._rng.random() < success_prob
            if success:
                boost = 0.1 * (1.0 - self.knowledge[concept])
                self.knowledge[concept] = self._clip(self.knowledge[concept] + boost)
                reward += 0.8 + self.knowledge[concept]
                child_output = "아이: 또박또박 \"아빠\"라고 불러요. 눈빛이 반짝입니다."
                self._last_success = True
                self._last_concept = concept
            else:
                reward -= 0.2
                child_output = "아이: 아직 그 단어가 낯설어 조용히 있어요."
                self._last_success = False
        elif action == "celebrate_success":
            if self._last_success and self._last_concept:
                concept = self._last_concept
                self.knowledge[concept] = self._clip(
                    self.knowledge[concept] + 0.06 * (1.0 - self.knowledge[concept])
                )
                reward += 1.2 + self.knowledge[concept]
                child_output = "돌봄이: 두 팔로 감싸 안으며 칭찬을 아낌없이 건넵니다."
                success = True
            else:
                reward -= 0.35
                child_output = "돌봄이: 아직 성공을 기다리는 중이라 조용히 격려합니다."
                success = False
                concept = self._last_concept
            self._last_success = False
        elif action == "soothing_encouragement":
            reward += 0.05
            child_output = "돌봄이: \"괜찮아, 천천히 해도 돼. 나는 네 편이야.\"라고 말해요."
            self._last_success = False

        self._log_step(
            step_index=self._step_count,
            action=action,
            reward=reward,
            child_output=child_output,
            success=success,
            concept=concept,
        )

        done = self._should_end()
        return self._observe(), reward, done, {
            "child_output": child_output,
            "success": success,
            "concept": concept,
            "knowledge": dict(self.knowledge),
        }

    def _should_end(self) -> bool:
        mastery = all(level >= self.mastery_threshold for level in self.knowledge.values())
        timeout = self._step_count >= self.max_steps
        return mastery or timeout

    @property
    def transcript(self) -> List[StepLog]:
        return list(self._transcript)


class CaretakerQLearner:
    """Tabular Q-learning caretaker that learns supportive routines."""

    def __init__(
        self,
        environment: VirtualChildEnvironment,
        learning_rate: float = 0.3,
        discount: float = 0.95,
        epsilon: float = 0.4,
        epsilon_decay: float = 0.995,
        min_epsilon: float = 0.05,
    ) -> None:
        self.environment = environment
        self.learning_rate = learning_rate
        self.discount = discount
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon
        self._q: Dict[State, Dict[ActionName, float]] = {}

    def _ensure_state(self, state: State) -> Dict[ActionName, float]:
        if state not in self._q:
            self._q[state] = {action: 0.0 for action in self.environment.ACTIONS}
        return self._q[state]

    def _select_action(self, state: State) -> ActionName:
        if random.random() < self.epsilon:
            return random.choice(self.environment.ACTIONS)
        q_values = self._ensure_state(state)
        return max(q_values, key=q_values.get)

    def _update(
        self,
        state: State,
        action: ActionName,
        reward: float,
        next_state: State,
        done: bool,
    ) -> None:
        q_values = self._ensure_state(state)
        next_values = self._ensure_state(next_state)
        best_next = 0.0 if done else max(next_values.values())
        target = reward + self.discount * best_next
        current = q_values[action]
        q_values[action] = current + self.learning_rate * (target - current)

    def train(
        self,
        episodes: int,
        max_steps: Optional[int] = None,
    ) -> Tuple[List[float], List[EpisodeLog]]:
        episode_rewards: List[float] = []
        sample_logs: List[EpisodeLog] = []
        sample_indices = {
            0,
            max(0, episodes // 2),
            max(0, episodes - 1),
        }

        for episode in range(episodes):
            state = self.environment.reset()
            total_reward = 0.0
            steps: List[StepLog] = []
            limit = max_steps or self.environment.max_steps

            for _ in range(limit):
                action = self._select_action(state)
                next_state, reward, done, info = self.environment.step(action)
                self._update(state, action, reward, next_state, done)
                total_reward += reward
                state = next_state

                step_log = StepLog(
                    step_index=len(steps) + 1,
                    action=action,
                    reward=reward,
                    child_output=str(info["child_output"]),
                    knowledge=dict(info["knowledge"]),
                    success=bool(info["success"]),
                    concept=info["concept"],
                )
                steps.append(step_log)

                if done:
                    break

            episode_rewards.append(total_reward)

            if episode in sample_indices:
                sample_logs.append(
                    EpisodeLog(
                        episode_index=episode,
                        total_reward=total_reward,
                        steps=steps,
                    )
                )

            self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)

        return episode_rewards, sample_logs

    def greedy_episode(self, max_steps: Optional[int] = None) -> EpisodeLog:
        """Run a deterministic episode using the learned policy."""

        state = self.environment.reset()
        steps: List[StepLog] = []
        total_reward = 0.0
        limit = max_steps or self.environment.max_steps

        for _ in range(limit):
            q_values = self._ensure_state(state)
            action = max(q_values, key=q_values.get)
            next_state, reward, done, info = self.environment.step(action)
            total_reward += reward
            steps.append(
                StepLog(
                    step_index=len(steps) + 1,
                    action=action,
                    reward=reward,
                    child_output=str(info["child_output"]),
                    knowledge=dict(info["knowledge"]),
                    success=bool(info["success"]),
                    concept=info["concept"],
                )
            )
            state = next_state
            if done:
                break

        return EpisodeLog(
            episode_index=-1,
            total_reward=total_reward,
            steps=steps,
        )


@dataclass
class TrainingStats:
    """Container for simulation training outputs."""

    episode_rewards: List[float]
    sampled_episodes: List[EpisodeLog]
    greedy_episode: EpisodeLog

    def reward_trend(self, window: int = 10) -> Tuple[float, float]:
        if not self.episode_rewards:
            return 0.0, 0.0
        head = self.episode_rewards[:window]
        tail = self.episode_rewards[-window:]
        head_avg = sum(head) / len(head)
        tail_avg = sum(tail) / len(tail)
        return head_avg, tail_avg

    def to_report(self) -> str:
        head_avg, tail_avg = self.reward_trend()
        lines: List[str] = [
            "# 가상 돌봄 강화학습 리포트",
            "",
            "가상의 아이가 "
            "\"철수는 바나나를 먹어요\"와 같은 문장을 연습하고, "
            "엄마·아빠 단어를 말했을 때 칭찬을 받도록 설계된 환경에서의 학습 결과입니다.",
            "",
            f"- 초기 10회 평균 보상: {head_avg:.3f}",
            f"- 마지막 10회 평균 보상: {tail_avg:.3f}",
            f"- 총 에피소드 수: {len(self.episode_rewards)}",
            "",
            "## 샘플 에피소드 대화",
        ]

        for episode in self.sampled_episodes:
            lines.append(f"### 에피소드 {episode.episode_index}")
            lines.append(f"총 보상: {episode.total_reward:.3f}")
            for step in episode.steps:
                lines.append(
                    f"- ({step.step_index}) {step.action} → 보상 {step.reward:.3f} | "
                    f"성공={step.success} | 아이 반응: {step.child_output}"
                )
            lines.append("")

        lines.append("## 학습된 정책 데모")
        lines.append(f"총 보상: {self.greedy_episode.total_reward:.3f}")
        for step in self.greedy_episode.steps:
            lines.append(
                f"- ({step.step_index}) {step.action} → 보상 {step.reward:.3f} | "
                f"아이 반응: {step.child_output}"
            )

        return "\n".join(lines)


def run_training(
    episodes: int,
    max_steps: Optional[int] = None,
    seed: Optional[int] = None,
) -> TrainingStats:
    """Train a caretaker policy and return the collected statistics."""

    environment = VirtualChildEnvironment(seed=seed)
    learner = CaretakerQLearner(environment=environment)
    rewards, samples = learner.train(episodes=episodes, max_steps=max_steps)
    greedy = learner.greedy_episode(max_steps=max_steps)
    return TrainingStats(
        episode_rewards=rewards,
        sampled_episodes=samples,
        greedy_episode=greedy,
    )


__all__ = [
    "VirtualChildEnvironment",
    "CaretakerQLearner",
    "TrainingStats",
    "run_training",
]

