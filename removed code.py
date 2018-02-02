


if index%100 == 0 and index > 0:  # Some molecules could give a ridiculous number of resonance structures
	# (e.g., [CH2]SC([S])=O). Here we apply filtering to `molList` (even if filter_structures=False) per 100
	# entries after the first 100 entrees (which are unfiltered) to speed up the resonance structures generation
	# and avoid significant slow-downs that some cases might trigger.
	molList = molList[:index] + filter_resonance_structures(molList[index:])
	
	
	
network.py debug:
	
@@ -548,22 +548,75 @@ class Network:
                 reac = products.index(rxn.reactants) + Nisom + Nreac
                 prod = isomers.index(rxn.products[0])
             else:
-                logging.info('\nUnexpected type of path reaction.')
-                logging.info('\nnetwork reactants:')
-                for react in reactants:
-                    logging.info(react[0].molecule[0].toAdjacencyList())
-                logging.info('network products:')
-                for pro in products:
-                    logging.info(pro[0].molecule[0].toAdjacencyList())
-                logging.info('network isomers:')
-                for iso in isomers:
-                    logging.info(iso.molecule[0].toAdjacencyList())
-                    logging.info(iso.molecule[0].reactive)
-                    logging.info(len(iso.molecule))
-                    for i in iso.molecule:
-                        logging.info(i.toAdjacencyList())
-                        logging.info(i.reactive)
-                        logging.info('\n')
+                # # Sometimes species are not identical after generating resonance structures due to unreactive structures
+                # # which may depend on the initial structure resonance structures were generated for (if it is an excited
+                # # state, it will be marked as unreactive, but if the initial structure is the ground state, unreactive
+                # # structures will not be generated). Before crashing, try to save this network by catching these cases:
+                # for rxn in self.pathReactions:
+                #     if rxn.reactants[0].is_structure_in_list(isomers) and rxn.products[0].is_structure_in_list(isomers):
+                #         # Isomerization
+                #         reac = isomers.index(rxn.reactants[0])
+                #         prod = isomers.index(rxn.products[0])
+                #     elif rxn.reactants[0].is_structure_in_list(isomers) and rxn.products.is_structure_in_list(reactants):
+                #         # Dissociation (reversible)
+                #         reac = isomers.index(rxn.reactants[0])
+                #         prod = reactants.index(rxn.products) + Nisom
+                #     elif rxn.reactants[0].is_structure_in_list(isomers) and rxn.products.is_structure_in_list(products):
+                #         # Dissociation (irreversible)
+                #         reac = isomers.index(rxn.reactants[0])
+                #         prod = products.index(rxn.products) + Nisom + Nreac
+                #     elif rxn.reactants.is_structure_in_list(reactants) and rxn.products[0].is_structure_in_list(isomers):
+                #         # Association (reversible)
+                #         reac = reactants.index(rxn.reactants) + Nisom
+                #         prod = isomers.index(rxn.products[0])
+                #     elif rxn.reactants.is_structure_in_list(products) and rxn.products[0].is_structure_in_list(isomers):
+                #         # Association (irreversible)
+                #         reac = products.index(rxn.reactants) + Nisom + Nreac
+                #         prod = isomers.index(rxn.products[0])
+
+
+                # logging.info('\nUnexpected type of path reaction.')
+                # logging.info('\nnetwork reactants:')
+                # for react in reactants:
+                #     logging.info('len(react): {0}'.format(len(react)))
+                #     for r in react:
+                #         logging.info('len(react.molecule): {0}'.format(len(r.molecule)))
+                #         for i in r.molecule:
+                #             logging.info(i.toAdjacencyList())
+                #             logging.info(i.reactive)
+                #             logging.info('\n')
+                # logging.info('network products:')
+                # for pro in products:
+                #     logging.info('len(pro): {0}'.format(len(pro)))
+                #     for p in pro:
+                #         logging.info('len(pro.molecule): {0}'.format(len(p.molecule)))
+                #         for i in p.molecule:
+                #             logging.info(i.toAdjacencyList())
+                #             logging.info(i.reactive)
+                #             logging.info('\n')
+                # logging.info('network isomers:')
+                # for iso in isomers:
+                #     logging.info('len(iso.molecule): {0}'.format(len(iso.molecule)))
+                #     for i in iso.molecule:
+                #         logging.info(i.toAdjacencyList())
+                #         logging.info(i.reactive)
+                #         logging.info('\n')
+                #
+                # logging.info('rxn.reactants:')
+                # for react in rxn.reactants:
+                #     logging.info('len(rxn.reactants): {0}'.format(len(rxn.reactants)))
+                #     for r in react.molecule:
+                #         logging.info(r.toAdjacencyList())
+                #         logging.info(r.reactive)
+                #         logging.info('\n')
+                # logging.info('rxn.products:')
+                # for pro in rxn.products:
+                #     logging.info('len(rxn.products): {0}'.format(len(rxn.products)))
+                #     for p in pro.molecule:
+                #         logging.info(p.toAdjacencyList())
+                #         logging.info(p.reactive)
+                #         logging.info('\n')
+
                 raise NetworkError('Unexpected type of path reaction "{0}"'.format(rxn))
         
             # Compute the microcanonical rate coefficient k(E)
			
			
			
			
			
+    def is_structure_in_list(self, species_list):
+        """
+        Return ``True`` if at least one molecule of the species is isomorphic with at least one molecule in at least
+        one spesies in 'species_list', which is a list of :class:`Species` objects.
+        """
+        for species in species_list:
+            if isinstance(species, Species):
+                for molecule1 in self.molecule:
+                    for molecule2 in species.molecule:
+                        if molecule1.isIsomorphic(molecule2):
+                            return True
+            else:
+                raise ValueError('Unexpected value "{0!r}" for species_list parameter;'
+                                 ' should be a List of Species objects.'.format(species))
+        return False


























