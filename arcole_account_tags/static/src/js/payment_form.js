/** @odoo-module **/

import PaymentForm from "@payment/js/payment_form";

PaymentForm.include({
  

    /**
     * Prepare the params for the RPC to the transaction route.
     *
     * @override method from payment.payment_form
     * @private
     * @return {object} The transaction route params.
     */
        _prepareTransactionRouteParams() {
            console.log("Arcole payment form _prepareTransactionRouteParams called");
            const transactionRouteParams =  this._super(...arguments);
            if (this.paymentContext['arcoleOid']) {
                transactionRouteParams['arcole_oid'] = this.paymentContext['arcoleOid'];
                transactionRouteParams['arcole_token'] = this.paymentContext['arcoleToken'];
            

                Object.assign(transactionRouteParams, {
                    'currency_id': this.paymentContext['currencyId']
                        ? parseInt(this.paymentContext['currencyId']) : null,
                    'partner_id': parseInt(this.paymentContext['partnerId']),
                    'reference_prefix': this.paymentContext['referencePrefix']?.toString(),
                });
            }
            return transactionRouteParams;
        },
});
