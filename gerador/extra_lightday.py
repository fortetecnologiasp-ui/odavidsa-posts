# Post avulso: o que o David falou no Light Day (iluminação para casamentos)
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from serie_base import X, UP
c = X("mkt", "light-day", "Light Day", "O que eu falei no Light Day",
  "Sem a <em>luz</em> certa, sua decoração some na foto",
  [("O detalhe que ninguém olha", ["A iluminação cênica e decorativa parece simples para quem monta o evento",
                                   "Mas é ela que muda o resultado da fotografia"]),
   ("Foto boa é portfólio", ["Uma ótima foto do seu trabalho vira vitrine para os próximos clientes",
                             "Ela vende o seu serviço mesmo quando você não está lá"]),
   ("Escute quem fotografa", ["O fotógrafo produz o material que todos os fornecedores vão usar",
                              "Ouvir o que ele precisa de luz é investir no seu próprio portfólio"]),
   ("O erro pequeno que custa caro", ["Ignorar a iluminação parece insignificante no dia do evento",
                                      "Mas deixa você atrás de quem entende o valor de uma boa foto"])],
  "No seu último evento, a luz ajudou ou atrapalhou as fotos?",
  "No Light Day eu falei sobre um detalhe que muitos profissionais de casamento ignoram: a iluminação cênica e decorativa. Ela muda a fotografia, e a fotografia é o portfólio de todo mundo que trabalhou naquele evento.",
  "Você trabalha com casamentos? Conta aqui",
  "#casamento #iluminacao #fotografiadecasamento #decoracaodecasamento #lightday")
c.update(foto=UP + "palestra-tela.jpg", foco="28% 35%", zoom=1.6)
c["legenda"] = c["legenda"].replace("👉 Siga @odavidsa",
  "🎤 Quer levar esse conteúdo para o seu evento ou equipe? Me chama no direct.\n\n👉 Siga @odavidsa")
c["cta"] = "Quer levar esse conteúdo para o seu evento ou equipe? Me chama no direct."
CARROSSEIS = [c]
