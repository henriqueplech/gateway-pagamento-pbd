O sistema trata-se de um Gateway de Pagamento intermediário entre lojistas e seus clientes. Lojistas são empresas ou pessoas físicas cadastradas na plataforma que desejam receber pagamentos de forma digital. Cada lojista possui uma taxa percentual definida, que representa o valor cobrado pelo gateway sobre cada transação processada, e pode cadastrar uma ou mais contas bancárias para receber seus repasses financeiros.

Clientes são os compradores que realizam pagamentos nas lojas cadastradas. Cada cliente pode registrar um ou mais métodos de pagamento, como cartões de crédito, que são armazenados de forma segura através de um token gerado pelo gateway, guardando apenas os últimos 4 dígitos e a bandeira do cartão para exibição.

Quando um cliente realiza uma compra em um lojista, o sistema registra uma transação contendo o valor bruto cobrado, o valor líquido após a dedução da taxa do gateway, o método de pagamento utilizado (cartão, PIX ou boleto) e o status do processamento, que pode ser Pendente, Aprovada, Recusada ou Cancelada. O payload retornado pela adquirente também é armazenado para fins de rastreabilidade.

Caso uma transação aprovada precise ser desfeita, o sistema registra um estorno vinculado àquela transação, contendo o valor a ser devolvido, o motivo e o status do processo de estorno.

Periodicamente, o gateway realiza repasses financeiros aos lojistas, consolidando o valor líquido das transações aprovadas e transferindo para a conta bancária cadastrada. Cada repasse possui uma data prevista e um status de processamento.
