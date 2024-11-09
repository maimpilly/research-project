[QueryItem="101"]
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
PREFIX : <http://www.semanticweb.org/owl/owlapi/turtle#>


SELECT *
WHERE {
  ?data_in_db :hasVoltageDrainSource ?voltage_drain_source .
  ?data_in_db :hasCondition ?condition .
  ?data_in_db :hasDataID ?id .
  ?data_in_db :hasGateLength ?gate_length .
}
[QueryItem="102"]
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
PREFIX : <http://www.semanticweb.org/owl/owlapi/turtle#>

SELECT  ?gateSource ?drainSource
WHERE {
  ?data rdf:type :data_in_db .
  ?data :hasVoltageGateSource ?gateSource .
  ?data :hasVoltageDrainSource ?drainSource .
}
[QueryItem="103"]
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
PREFIX : <http://www.semanticweb.org/owl/owlapi/turtle#>

SELECT *
WHERE {
  ?data :hasCondition ?condition .
  ?data :hasDataID ?id .
  FILTER (?condition = 'intact')
}