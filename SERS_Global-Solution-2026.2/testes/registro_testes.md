# Registro de testes com usuários — SERS

**Situação atual:** A PREENCHER COM TESTES REAIS. O enunciado de SERS pede situações testadas, compreensão, utilidade, comentários e ajustes; não fixa número mínimo de pessoas.

## Passos para executar

1. Execute `python3 web_app.py` e abra `http://127.0.0.1:8000/usuario`.
2. Convide um colega que não seja integrante. Cada pessoa recebe um identificador anônimo (`P-...`). Não registre nomes, e-mails ou telefones.
3. Peça para testar, com suas palavras, os três cenários: **consumo do notebook**, **economia de energia**, **se solar vale a pena**.
4. Depois de cada resposta, pergunte: "Você entendeu os números e as limitações?" e "A orientação foi útil? Por quê?". No chatbot, marque útil/não útil e conclua a sessão; aqui, transcreva o comentário de forma fiel.
5. Se houve dificuldade, ajuste a `resposta` ou uma `palavra_chave` no JSON; reinicie o servidor para carregar o arquivo e repita a pergunta. Anote o antes/depois. Se não houve ajuste, documente a justificativa real.

## Resultados (preencher, sem inventar)

| ID anônimo | Situação perguntada | Encontrou? | Compreendeu? | Útil? | Comentário REAL | Ajuste REAL |
|---|---|---|---|---|---|---|
| [P-...] | Consumo | [sim/não] | [sim/não] | [sim/não] | [comentário] | [ajuste/nenhum] |
| [P-...] | Eficiência | [sim/não] | [sim/não] | [sim/não] | [comentário] | [ajuste/nenhum] |
| [P-...] | Solar | [sim/não] | [sim/não] | [sim/não] | [comentário] | [ajuste/nenhum] |

## Síntese a preencher depois

**Quantidade de participantes distintos:** [N]  
**Consultas concluídas:** [N]  
**Feedback sobre compreensão:** [descrever sem fabricar]  
**Feedback sobre utilidade:** [descrever sem fabricar]  
**Problema encontrado:** [situação real, se houve]  
**Alteração feita:** [alteração real, se houve; caso contrário justificar]  
**Repetição da pergunta após a alteração:** [resultado real]

> Preencha com avaliações reais feitas sobre as orientações de energia. Não inclua dados pessoais desnecessários.
