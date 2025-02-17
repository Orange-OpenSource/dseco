#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  Copyright (c) 2023-2025 Orange. All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
#      1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#      2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#      3. All advertising materials mentioning features or use of this software must display the following acknowledgement:
#      This product includes software developed by Orange.
#      4. Neither the name of Orange nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY Orange "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL Orange BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

# test_base.py
from behave import given, when, then
import rdflib
from rdflib.plugins.sparql import prepareQuery
import owlrl


def print_diff(liste1, liste2):
    set1 = set(liste1)
    set2 = set(liste2)

    l1 = len(set1)
    l2 = len(set2)

    if l1 > l2:
        for item in set1 - set2:
            print(f"- {item}")
    elif l2 > l1:
        for item in set2 - set1:
            print(f"- {item}")
    elif l2 == l1:
        for item in set2 - set1:
            print(f"- {item}")
        for item in set1 - set2:
            print(f"+ {item}")
    

@given('that the KG is loaded and the reasoner applied')
def step_impl(context):
    # Initialisation du graphe RDF
    context.graph = rdflib.Graph()

    # Chargement de l'ontologie et des données dans le graphe pour le test 01
    context.graph.parse("datatest.ttl", format="turtle")

    # Application du raisonnement OWL-RL
    owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(context.graph)

@when("I run SPARQL query located at {sparql_query_file} to gather entries with WhoisDomain is example.org")
@when("I run SPARQL query located at {sparql_query_file} to gather entries with WhoisDomain is example.org and their final resolution")
@when("I run SPARQL query located at {sparql_query_file} to gather FQDN belongings to zone example.org and that a intermediary or final witch is not managed by Org top nor Org int")
@when("I run SPARQL query located at {sparql_query_file} to gather entries of example.org that do not resolve at all at the end")
@when("I run SPARQL query located at {sparql_query_file} to gather entries managedBy Org int that do not have a corresponding in Org top")
@when("I run SPARQL query located at {sparql_query_file} to gather entries managedBy Org int that do not have a corresponding in Org top and that have a A to an IP")
@when("I run SPARQL query located at {sparql_query_file} to list all the IP address")
@when("I run SPARQL query located at {sparql_query_file} to gather entries that loops to themselves")
def step_impl(context, sparql_query_file):
    # Chargement de la requête SPARQL à partir du fichier
    with open(sparql_query_file, "r") as file:
        context.query = prepareQuery(file.read())
    tempresults = list(context.graph.query(context.query))
    
    sparql_r = []
    for  result in tempresults:
        s = " ".join(result)
        sparql_r.append(s)
    context.sparql_results = sorted(sparql_r)

    #context.sparql_results = sorted([[str(column) for column in result] for result in tempresults])

@then('I should obtain the results from file {expected_results_file}')
def step_impl(context, expected_results_file):
    # Chargement des résultats attendus à partir du fichier CSV pour le test 01
    with open(expected_results_file, "r") as file:
        lines = [line.rstrip() for line in file]
        context.expected_results = sorted(lines)

    print('')
    print('diff between sparql_results and expected_results ')
    print('')
    print_diff(context.sparql_results , context.expected_results)
    print(' ')
    print(' ')

    # Verification of the alignment between actual results and expected outcomes for Test 01.
    assert context.sparql_results == context.expected_results, "La requête SPARQL n'a pas retourné les résultats attendus."

