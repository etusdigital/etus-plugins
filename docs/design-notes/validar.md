# Validar o sistema

O que eu preciso garantir antes de dar como pronto o meu sistema:

- [ ] Garantir que os eventos que eu coleto chegam corretamente no Collector e que eles sejam salvos no R2 Raw
- [ ] Garantir que estou coletando todos os eventos com as propriedades que eu preciso em cada um dos módulos do SDK Web
- [ ] Validar todas as propriedades de cada evento planejado esteja sendo enviadas para o Collector
- [ ] Garantir que eu estou interceptando todos os requests de arquivos html na minha cloudflare para todos os meus domínios
- [ ] Garantir que ao interceptar os requests eu colete:
  - [ ] todos os campos que a Cloudflare oferece
    - [ ] todos os cookies de 3P
    - [ ] Todos os headers http
    - [ ] Todos os headers de client hints quando disponiveis
    - [ ] Gere o ID Sessão quando nao existir o cookie
    - [ ] Gere o Anonymous ID quando nao existir o cookie
    - [ ] Gere o Pageview ID e o Interception ID para todo request
    - [ ] Colete o User ID quando ele existir nos cookies ou no server side do meu sistema
    - [ ] Colete todos os query params da url e separe cada um deles e sempre salve o total deles
    - [ ] Colete o User Agent do browser
    - [ ] Identifique query strings gigantes e possa filtrar eles por meio de configs predefinidas
    - [ ] Insira o contexto no browser no inicio do head do html de uma forma hasheada ou obfuscada
    - [ ] Gere o distinct ID com elementos mais deterministicos tipo o que o Umami faz
    - [ ] Consiga fazer a detecção de bots mais leves sem prejudicar a latencia do usuario usando o pacote de bot detection do ETS
    - [ ] Consiga gerenciar split de versoes para testes A/B orientado a canary deployment
    - [ ] Consiga injetar o SDK no inicio do head do html quando a configuração existir para aquele dominio
    - [ ] Consiga criar e editar os cookies das plataformas da ETUS
    - [ ] Sempre tenha logs para capturar os timings
    - [ ] Tenha logs para todas as excecoes e erros para monitoramento e debugging
- [ ] Garantir que todo o sistema utilize os eventos e propriedades do Catalog
- [ ] Garantir que todo o meu sistema utilize os tracking plans para seus dominios
- [ ] Conseguir debugar o funcionamento do SDK no browser com o modo debug ativado
- [ ] Garantir que nao estou perdendo nenhum evento coletado pelo SDK no browser
- [ ] Garantir que nenhum evento dispare antes do pageview ser gerado
- [ ] Garantir que os eventos de track e identity sempre façam o merge do contexto do pageview onde foram disparados
- [ ] Garantir que o contexto de uma sessão seja persistido durante qualquer navegacao do usuario em outras páginas do mesmo dominio
- [ ] Implemente o Linker para capturar eventos cross domain mantendo o contexto da sessão e do usuario
- [ ] Garantir que os eventos salvos no R2 Raw sejam processados depois para parquet criando o Bronze
- [ ] Poder habilitar o challenge da cloudflare para usuarios suspeitos
- [ ] Poder filtrar páginas ou paths que eu quero que o interceptor nao intercepte ou intercepte
- [ ] Garantir que todos os dados que forem gerados para o bronze também sejam enviados para o Clickhouse

## Primeiro

Eu quero conseguir validar cada etapa localmente criando um banco de dados local para testes e debug e simular o endpoint do collector para eu poder testar cada etapa isoladamente. Antes de qualquer coisa eu preciso validar a coleta dos eventos e as propriedades que eu preciso em cada um dos módulos do SDK Web.

## Segundo

Depois de validar a coleta e envio correto para o collector, eu preciso validar que o RAW data esteja sendo salvo no R2 Raw exatamente como chegou no collector
