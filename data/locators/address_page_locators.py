


class AddressPageLocators:

    country = 'input[placeholder="Please provide a country."]'
    name = 'input[placeholder="Please provide a name."]'
    mobile_number = 'input[placeholder="Please provide a mobile number."]'
    zip_code = 'input[placeholder="Please provide a ZIP code."]'
    address = 'textarea[placeholder="Please provide an address."]'
    city = 'input[placeholder="Please provide a city."]'
    state = 'input[placeholder="Please provide a state."]'
    submit_btn = 'button#submitButton'
    back_btn = 'button:has-text("Back")'
    continue_btn = 'button[aria-label="Proceed to payment selection"]'

    created_address = 'mat-row mat-cell'

    toast = 'simple-snack-bar .mat-mdc-snack-bar-label'

    #saved_addresses

    add_new_address_btn = 'button[aria-label="Add a new address"]'
    edit_btn = 'mat-cell.mat-column-Edit button'
    delete_address_btn = 'mat-cell.mat-column-Remove button'
    random_address = 'mat-row'
    created_name = 'mat-cell.mat-column-Name'
    created_address_name = 'mat-cell.mat-column-Address'
    created_country = 'mat-cell.mat-column-Country'


def quick_sort(nums: list[int]) -> list[int]:
    if len(nums) <= 1:
        return nums

    pivot = nums[len(nums) // 2]
    left = [x for x in nums if x < pivot]
    middle = [x for x in nums if x == pivot]
    right = [x for x in nums if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

print(quick_sort([3, 1, 4, 1, 5, 9]))


