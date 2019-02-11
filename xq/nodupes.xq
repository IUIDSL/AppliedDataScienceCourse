(: Open XML files 3 and 4:)
let $xs := (doc('cricket-xml-3.xml'),doc('cricket-xml-4.xml'))

(: Get all distinct ID values:)
let $mids := fn:distinct-values(
 for $match in $xs/matches/match
 where $match/ball/@batting="England"
 order by $match/@mid
 return $match/@mid)

(: For every distinct ID value, return the first match that matches that ID:)
let $dms := (
for $id in $mids
let $mms := (for $match in $xs/matches/match
            where $match/@mid=$id
            return $match)[1]
return $mms )

(: Loop through all balls, return sum of runs if England was batting:)
return fn:sum(
for $ball in $dms/ball
where $ball/@batting = "England"
return $ball/@runs)