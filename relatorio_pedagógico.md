# Relatório Pedagógico do Plugin Gamificado

## 1. Identificação do Plugin

**Nome do jogo/plugin:** RPG Turing Quiz

**Área da disciplina:** Computabilidade e Complexidade de Algoritmos

**Grupo:**

- Nome: Leonardo Nascimento de Oliveira
- RA: 33356441

- Nome: Lucas Messias Marques
- RA: 34190058

- Nome: Nicolas Gabriel da Silva Josafá
- RA: 34693718

---

## 2. Objetivo Pedagógico

O jogo visa trabalhar conceitos fundamentais de máquinas de Turing e resolução de problemas computacionais complexos. Ao participar, o aluno deverá aprender e praticar a identificação das funções e limites das máquinas de Turing, bem como classificar problemas computacionais segundo critérios da teoria da computação. O jogo estimula o raciocínio lógico e a aplicação de algoritmos em situações gamificadas.

---

## 3. Descrição do Jogo

O RPG Turing Quiz consiste em uma série de desafios apresentados em formato de perguntas e respostas, com progressão temática inspirada em RPG. Cada rodada apresenta um problema/algoritmo ao aluno, que deve indicar se ele pode ser resolvido por uma máquina de Turing e justificar. O tempo estimado de cada partida é de 20 minutos. O aluno recebe feedback imediato ao responder, por meio de mensagens de acerto, erro, dicas e pontuação final.

---

## 4. Conteúdo Relacionado à Disciplina

**Tópicos abordados:**

- Máquinas de Turing e suas variações
- Decidibilidade e reconhecibilidade
- Problemas NP-completo
- P vs NP
- Notação assintótica (Big O)

O jogo contribui para a compreensão prática dos limites computacionais, classificação de problemas e entendimento dos impactos da decidibilidade na computação moderna. Os alunos vivenciam situações que envolvem a análise de algoritmos e a aplicação dos conceitos de complexidade computacional.

---

## 5. Critérios de Pontuação

A pontuação é baseada no número de respostas corretas. Cada acerto concede pontos, e erros podem resultar em penalidades na pontuação. Dicas solicitadas reduzem a pontuação atual. O tempo para resolver cada desafio impacta na nota final: partidas rápidas sem erros recebem maior pontuação. O mínimo para aprovação é 60% dos pontos totais; penalidades podem ser aplicadas por respostas incorretas, excesso de dicas ou extrapolação do tempo limite.

---

## 6. Testes Realizados

1. **Caso de acerto total:** Usuário responde corretamente todas as perguntas, sem solicitar dicas.
2. **Erro esperado:** Usuário responde incorretamente problemas conhecidos de indecidibilidade.
3. **Tempo limite excedido:** Usuário não finaliza o desafio dentro do tempo; pontuação reduzida.
4. **Repetição com mesma seed:** Rodada iniciada com o mesmo parâmetro de aleatoriedade garante repetibilidade dos desafios.
5. **Solicitação de dicas:** Usuário utiliza dicas para algumas perguntas, recebendo penalidades previstas.

---

## 7. Roteiro de Demonstração

A apresentação será realizada em dois cenários:

- **Cenário feliz:** Usuário simula uma partida ideal, utilizando o conhecimento adquirido para obter pontuação máxima.
- **Cenário de erro:** Usuário deliberadamente comete erros e solicita dicas, demonstrando penalidades e feedback de aprendizado proporcionados pelo plugin.
