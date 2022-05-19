----- Bee Cards ------


SELECT a.clientid,
    (SELECT COUNT(*) FROM SL_CARD WHERE cardid IS NOT NULL and clientid = a.clientid) as TotalCount,
    (SELECT COUNT(*) FROM SL_CARD WHERE state='1' and clientid = a.clientid) as TotalIssued,
    (SELECT COUNT(*) FROM (select distinct b.cardholderid,b.clientid  from SL_CARD b WHERE b.cardholderid IS NOT NULL ) where clientid = a.clientid ) as Registered,
    round(((SELECT COUNT(*) FROM (select distinct b.cardholderid,b.clientid  from SL_CARD b WHERE b.cardholderid IS NOT NULL ) where clientid = a.clientid )/(SELECT COUNT(*) FROM SL_CARD WHERE state='1' and clientid = a.clientid))*100) as Percent_Registered,
    (SELECT COUNT(*) FROM SL_CARD WHERE state='1' and clientid = a.clientid)-(SELECT COUNT(*) FROM (select distinct b.cardholderid,b.clientid  from SL_CARD b WHERE b.cardholderid IS NOT NULL ) where clientid = a.clientid ) as UNREGISTERED_ISSUED,
    (SELECT COUNT(*) FROM SL_CARD WHERE cardid IS NOT NULL and clientid = a.clientid)-(SELECT COUNT(*) FROM SL_CARD WHERE state='1' and clientid = a.clientid) as UNISSUED 
FROM (SELECT DISTINCT clientid FROM SL_CARD) a
GROUP BY clientid
ORDER BY clientid;
