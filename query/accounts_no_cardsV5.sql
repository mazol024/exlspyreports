
---------------------no cards accounts-----------
SELECT
   DISTINCT contr.contractnumber, cusacc.username,  adr.city, adr.postalcode
FROM sl_customeraccount cusacc 
LEFT JOIN sl_contract contr on cusacc.contractid = contr.contractid
LEFT JOIN sl_cardtocontract car2con on car2con.contractid = cusacc.contractid
LEFT JOIN sl_contractaddress conaddr on contr.contractid = conaddr.contractid
LEFT JOIN sl_address adr on adr.addressid = conaddr.addressid
where contr.state = 1
and car2con.cardid is null 
and conaddr.addresstype = 1
and cusacc.state = 1
order by 1;