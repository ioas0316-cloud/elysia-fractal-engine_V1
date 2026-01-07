from Core.Foundation.web_knowledge_connector import WebKnowledgeConnector

w = WebKnowledgeConnector()
m = w.comm_enhancer.get_communication_metrics()
print(f'현재 어휘: {m["vocabulary_size"]}개')
print(f'패턴: {m["expression_patterns"]}')
print(f'템플릿: {m["dialogue_templates"]}')
