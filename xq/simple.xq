fn:sum(
 let $doc := (doc("../data/cricket-xml-3.xml"), doc("../data/cricket-xml-4.xml"))
 for $ball in $doc/matches/match/ball
 where $ball/@batting = "England"
 return $ball/@runs
)