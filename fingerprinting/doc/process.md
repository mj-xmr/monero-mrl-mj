
A) = used by
B) = uses

I) monero_fee_utils::calculate_fee

1) monero_fee_utils::calculate_fee:
A) monero_transfer_utils::send_step2__try_create_transaction monero_transfer_utils.cpp.o
B) - monero_fee_utils::calculate_fee_from_weight
	 - cryptonote::get_transaction_weight
	 - monero_fee_utils::calculate_fee_from_size

2) send_step2__try_create_transaction
A) _reenterable_construct_and_send_tx ./monero_send_routine.cpp.o 
B) 


3) _reenterable_construct_and_send_tx
A) - Externally? TODO: Verify
	 - Recursively


Next steps:
search for:
- monero_fee_utils::calculate_fee_from_weight
- monero_fee_utils::calculate_fee_from_size



II) monero_fee_utils::calculate_fee_from_weight

1) monero_fee_utils::calculate_fee_from_weight
A) monero_fee_utils::estimate_fee
B) none

III) monero_fee_utils::estimate_fee

1) monero_fee_utils::estimate_fee
A) - monero_transfer_utils::send_step1__prepare_params_for_get_decoys  --- MORE
B) - monero_fee_utils::estimate_rct_tx_size





git-tags-dates.sh | sort >  ~/devel/pub-lc/scripts/monero/monero-mrl-mj/testnet-framework/doc/tags.md

Search subspace to prove differences:

2018-10-18 | v1.1.1 		| v9 compat
2018-10-23 | v1.1.2 		| v9 fee updates

======== 

gc v1.1.2
gd v1.1.1

--- a/local_modules/SendFundsTab/Views/SendFundsView_Base.web.js
+++ b/local_modules/SendFundsTab/Views/SendFundsView_Base.web.js
@@ -934,7 +934,7 @@ class SendFundsView extends View
        {
                const self = this
                const estimatedNetworkFee_JSBigInt = new JSBigInt(self.context.monero_utils.estimated_tx_network_fee(
-                       "187000000", // TODO: grab this from polling request for dynamic per kb fee
+                       "25190000", // TODO: grab this from polling request for dynamic per kb fee
                        self._selected_simplePriority()
                ))
                
                
--- a/local_modules/mymonero_core_js
+++ b/local_modules/mymonero_core_js
@@ -1 +1 @@
-Subproject commit 9c20339f1914321fa44227b41d5da087f8f225e3
+Subproject commit 789c1fa71b00fa0579389b7a9f483877745fb06c

pushd mymonero-app-js 		&& git-tags-dates.sh 	mm-app-js-	| sort -r > ~/devel/pub-lc/scripts/monero/monero-mrl-mj/testnet-framework/doc/tags/tags-mm-app-js.txt 	&& popd
pushd mymonero-core-cpp 	&& git-tags-dates.sh 	mm-core-cpp-t  	| sort -r > ~/devel/pub-lc/scripts/monero/monero-mrl-mj/testnet-framework/doc/tags/tags-mm-core-cpp.txt	&& popd
pushd mymonero-core-cpp 	&& git-commits-dates.sh mm-core-cpp-c  	| sort -r > ~/devel/pub-lc/scripts/monero/monero-mrl-mj/testnet-framework/doc/tags/commits-mm-core-cpp.txt	&& popd
pushd mymonero-core-js-mj 	&& git-commits-dates.sh mm-core-js 	| sort -r > ~/devel/pub-lc/scripts/monero/monero-mrl-mj/testnet-framework/doc/tags/commits-mm-core-js.txt 	&& popd
pushd monero-orig 		&& git-tags-dates.sh 	monero-core	| sort -r > ~/devel/pub-lc/scripts/monero/monero-mrl-mj/testnet-framework/doc/tags/monero.txt 		&& popd

cd ~/devel/pub-lc/scripts/monero/monero-mrl-mj/testnet-framework/doc/tags
cat *.txt | sort -r > all/tags-all.txt
