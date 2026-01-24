

class DigitalWalletPageLocators:

    amount_field = 'input[aria-label="Enter an amount"]'
    deposit_btn = 'button[aria-label="Button to continue to payment"]'
    sum_text = 'b span.confirmation'
    select_card_radio_btn = 'mat-radio-button'
    continue_btn = 'button[aria-label="Proceed to review"]'
    crypto_wallet_link = 'a:has-text("Try out our new Crypto Wallet")'

    toast = 'simple-snack-bar .mat-mdc-snack-bar-label'

    #crypto_walllet
    amount_field_crypto = 'input#inputAmount'
    deposit_crypto_btn = 'button[aria-label="Button to deposit"]'
    connect_metamask_btn = 'button:has-text("Connect your MetaMask")'