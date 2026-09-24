import unittest
from unittest.mock import patch
from nexo.core import Retriever, answer, chunks, contextual_query, cosine, load_documents

class CoreTests(unittest.TestCase):
    def test_chunk_overlap_preserves_words(self):
        doc={**load_documents()[0],'text':' '.join(str(i) for i in range(250))}
        result=chunks([doc])
        self.assertEqual(result[0]['text'].split()[-20:],result[1]['text'].split()[:20])
        self.assertEqual(result[-1]['text'].split()[-1],'249')

    def test_no_evidence(self):
        self.assertEqual(answer('capital Finlandia')['status'],'sin_evidencia')

    def test_external_internal_retrieval(self):
        items=Retriever().search('reportar correo sospechoso phishing NIST')
        self.assertEqual({d['kind'] for d in items},{'interna','externa'})

    def test_followup(self):
        query=contextual_query('¿Y cuánto demora?', [{'question':'Tengo una falla de VPN'}])
        self.assertIn('VPN',query)

    def test_new_topic_does_not_keep_history(self):
        self.assertEqual(contextual_query('Perdí el teléfono de autenticación MFA',[{'question':'VPN'}]),'Perdí el teléfono de autenticación MFA')

    def test_input_limit(self):
        with self.assertRaises(ValueError):answer('x'*1001)

    def test_cosine_dimensions(self):
        with self.assertRaises(ValueError):cosine([1],[1,2])

    def test_invalid_citation_rejected(self):
        engine=Retriever()
        with patch.object(engine,'search',return_value=[{**load_documents()[0],'chunk_id':'INT-01:0','sha256':'a'}]),patch('nexo.core.ollama',return_value={'message':{'content':'Entrega tu clave [FAKE-99:0]'}}):
            self.assertEqual(answer('recuperar contraseña',mode='llm',retriever=engine)['status'],'revision_requerida')

    def test_missing_citation_rejected(self):
        engine=Retriever()
        with patch.object(engine,'search',return_value=[{**load_documents()[0],'chunk_id':'INT-01:0'}]),patch('nexo.core.ollama',return_value={'message':{'content':'La clave cambia mañana.'}}):
            self.assertEqual(answer('recuperar contraseña',mode='llm',retriever=engine)['status'],'revision_requerida')

if __name__=='__main__':unittest.main()
