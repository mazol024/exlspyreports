-----------First Sheet ----------

SELECT * from mobile;

----------- Cards which are registered (with dbocard holder) and which do not have any card action with a date of birth set ------------ 

select CardId
from SL_Card 
where SerialNumber in
(
    select TO_CHAR(CardNo)
    from
    (
        select CardNo, Sum(countDOB) as sumCountDOB
        from
        (
            select CardNo, count(DateOfBirth) as countDOB
            from PP_CardActionRequest, PP_CardActionAttribute
            where PP_CardActionAttribute.CardActionRequestId = PP_CardActionRequest.id
            group by CardNo, DateOfBirth
        )
        group by CardNo
    )
    where sumCountDOB = 0 
    and CardNo in
        (
            select serialNumber
            from SL_Card
            where CardHolderId is not null
            and SerialNumber not like '-%'
        )
)
order by CardId;

----------- Cards which are registered (with card holder) and which do not have any card action with a registration set ------------ 
select CardId
from SL_Card 
where SerialNumber in
(
    select TO_CHAR(CardNo)
    from
    (
        select CardNo, Sum(countREG) as sumCountREG
        from
        (
            select CardNo, count(Registration) as countREG
            from PP_CardActionRequest, PP_CardActionAttribute
            where PP_CardActionAttribute.CardActionRequestId = PP_CardActionRequest.id
            group by CardNo, Registration
        )
        group by CardNo
    )
    where sumCountREG = 0 
    and CardNo in
        (
            select serialNumber
            from SL_Card
            where CardHolderId is not null
            and SerialNumber not like '-%'
        )
)
order by CardId;
