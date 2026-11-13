# Cuida+ — Roteiro do vídeo pitch (até 3 minutos)

> Cerca de 420 palavras, aproximadamente 2 min 50 s em ritmo calmo.
> Narração: Will Pereira (RM576183). Se possível, apareça na câmera no início ou no fim.
> Telas sugeridas: grave a tela mostrando os slides indicados entre colchetes.
> A modelagem de dados **não** precisa aparecer no vídeo.

---

### 0:00 – 0:25 · Gancho e problema  [slides 1 e 3]
O Brasil tem mais de 32 milhões de pessoas com 60 anos ou mais. Muitas tomam vários remédios por dia, e quase 1 em cada 5 idosos usa cinco ou mais. Só que a adesão a tratamentos crônicos fica perto de 50%: metade das doses se perde no esquecimento.

E marcar uma consulta ou um corte de cabelo? Telefone ocupado, aplicativo com letra pequena, muitos passos. O resultado é perda de autonomia e uma família preocupada à distância.

### 0:25 – 0:45 · Persona  [slide 4]
Pense na Dona Maria, 74 anos. Ela mora sozinha, toma quatro remédios e prefere falar a digitar. A filha dela, a Carla, liga todo dia só para perguntar: "mãe, tomou o remédio?".

### 0:45 – 1:05 · A solução  [slides 5 e 6]
Para elas eu criei o **Cuida+**, uma plataforma web CitizenTech com uma assistente de voz que conversa, lembra e agenda. Ela conecta três pontas: a pessoa idosa, a família e os prestadores do bairro, como médicos, salões, farmácias e comércios, que publicam suas agendas na plataforma.

### 1:05 – 1:55 · Demonstração do protótipo  [slides 10 a 15]
Na tela inicial, a Dona Maria vê os remédios do dia por cor e um botão grande: "Falar com a Cuida".
Ela diz: *"Quero cortar o cabelo terça de manhã, perto de casa."*
A IA transcreve a fala, entende o pedido e consulta os horários livres reais dos salões próximos. Depois oferece só duas opções, para não confundir.
Um ponto importante: **nada é marcado sem confirmação**. A tela mostra o que a IA entendeu, e ela responde "pode marcar".
O salão recebe o pedido na agenda, já com as observações de acessibilidade, e confirma. A Dona Maria recebe lembretes um dia e uma hora antes.
Na hora do remédio, um alerta em tela cheia aparece, e ela responde "já tomei", falando ou tocando no botão.

### 1:55 – 2:25 · Inteligência artificial  [slides 16, 21 e 22]
A IA trabalha em duas frentes. A primeira é a **assistente de agendamento por voz**. A segunda é um **monitor preditivo de adesão**: com o histórico de doses, ela percebe padrões, como "a dose das 20h é esquecida nos dias em que a Dona Maria sai de casa à tarde", e sugere à Carla mudar o lembrete para 19h30.
A família recebe alerta só quando há risco real. É cuidado, não vigilância. A IA não faz diagnóstico, e a decisão é sempre humana.

### 2:25 – 2:50 · Impacto e ODS  [slides 23 e 24]
Vamos medir o impacto com dados da própria plataforma. As metas do piloto de seis meses são:
- adesão aos remédios acima de 85%;
- 60% dos agendamentos feitos pelo próprio idoso;
- faltas abaixo de 10%;
- agendamento em menos de 2 minutos.

O projeto se conecta aos **ODS 3** (saúde e bem-estar), **10** (redução das desigualdades) e **11** (cidades e comunidades sustentáveis).

### 2:50 – 3:00 · Fechamento  [slide 27]
Cuida+: a tecnologia fala a língua de quem mais precisa.
Obrigado!

---

**Checklist antes de entregar**
- [ ] Publicar o vídeo no YouTube como **Público** e testar o link em uma aba anônima.
- [ ] Trocar `VIDEO_URL` em `gerar_apresentacao_cuidamais.py`, ou editar o último slide no PowerPoint, e exportar o PDF novamente (`exportar_pdf.ps1`).
- [ ] Se houver campo para arquivos complementares: no Oracle SQL Developer Data Modeler, use *File → Import → DDL File* com `modelo_dados/cuidamais_ddl.sql`, salve o projeto e compacte em `.zip`.
