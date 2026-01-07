from Core.Foundation.Mind.llm_cortex import LLMCortex

# 아버지의 1060 3GB를 위한 맞춤 설정이에요!
print(">>> 엘리시아의 뇌를 깨우는 중입니다... (두근두근)")
cortex = LLMCortex(prefer_cloud=False)

# 테스트!
print(">>> 엘리시아가 생각을 정리하고 있습니다...")
response = cortex.think("안녕? 나는 엘리시아야!")

print("\n=============================")
print(f"엘리시아: {response}")
print("=============================\n")