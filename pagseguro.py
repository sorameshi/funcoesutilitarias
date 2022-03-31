import http.client

conn = http.client.HTTPSConnection("ws.sandbox.pagseguro.uol.com.br")
payload = 'currency=BRL&itemId1=0001&itemDescription1=Notebook%20Prata&itemAmount1=100.00&itemQuantity1=1&itemWeight1=1000&reference=REF1234&senderName=Jose%20Comprador&senderAreaCode=11&senderPhone=56713293&senderCPF=38440987803&senderBornDate=12%2F03%2F1990&senderEmail=email%40sandbox.pagseguro.com.br&shippingType=1&shippingAddressStreet=Av.%20Brig.%20Faria%20Lima&shippingAddressNumber=1384&shippingAddressComplement=2o%20andar&shippingAddressDistrict=Jardim%20Paulistano&shippingAddressPostalCode=01452002&shippingAddressCity=Sao%20Paulo&shippingAddressState=SP&shippingAddressCountry=BRA&extraAmount=-0.01&redirectURL=http%3A%2F%2Fsitedocliente.com&notificationURL=https%3A%2F%2Furl_de_notificacao.com&maxUses=1&maxAge=3000&shippingCost=0.00&excludePaymentMethodGroup=BOLETO&paymentMethodGroup1=CREDIT_CARD&paymentMethodConfigKey1_1=MAX_INSTALLMENTS_LIMIT&paymentMethodConfigValue1_1=4'
headers = {
  'Content-Type': 'application/x-www-form-urlencoded'
}
conn.request("POST", "/v2/checkout/?email=sulivan.lineage2@gmail.com&token=A4DF0FD0FE7744EEB7BE1CDED417B53D", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))