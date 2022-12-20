from flask import render_template, flash, redirect, url_for, request

from app import app
from app.api_data_access import TemplateAPI
from app.forms import OptionInitializeDataForm, OptionImportDataForm
import time
import json

PERMISSION_DENIED = 'You do not have permission to view this page.'
GENERAL_ERROR = 'An error occured, please try again later.'
PAGE_NOT_FOUND = 'Page not found'
APPLICATION_ERROR = 'An application error occured, please try again later.'


# We won't route to a dashboard/landing page but if you do
# then route '/' and '/index' here and amend dashboard.html:
@app.route('/dashboard')
def dashboard():
    # Get example data from API
    options_list = TemplateAPI.list()
    # That is an array if it worked, if not it is normal JSON with an error key
    if isinstance(options_list, list):
        return render_template('dashboard.html', options_list=options_list)
    else:
        error = options_list.get('error')
        return render_template('error.html', error=error)


@app.route('/')
@app.route('/index')
@app.route('/options_list')
def options_list():
    # Get example data from API
    options_list = TemplateAPI.list()
    # That is an array if it worked, if not it is normal JSON with an error key
    if isinstance(options_list, list):
        return render_template('options_list.html', options_list=options_list)
    else:
        error = options_list.get('error')
        return render_template('error.html', error=GENERAL_ERROR)


@app.route('/option_add', methods=['GET', 'POST'])
def option_add():
    # Default start and exipry to now (you can change this if needed):
    start = int(time.time())
    expiry = start
    form = OptionInitializeDataForm(start=start, expiry=expiry)
    if form.validate_on_submit():
        contract_size = form.contract_size.data
        coll_asset = form.coll_asset.data
        settle_asset = form.settle_asset.data
        start = form.start.data
        expiry = form.expiry.data
        strike_price = form.strike_price.data
        try:
            new_entry = TemplateAPI.option_add(contract_size, coll_asset, settle_asset, start, expiry, strike_price)
            if not (new_entry.get('error') is None):
                flash(new_entry.get('error'), 'error')
                return render_template('option_add.html', title='New Option', form=form, already_entered=False)
            print(new_entry)
            contract_id = new_entry['contract_id']
            flash(f'Created new contract. Contract ID: {contract_id}', 'success')
            return redirect(url_for('options_list'))
        except ValueError as e:
            # This duplicate test isn't implemented in this example but if you
            # want to then implement in API layer (although there is likely no
            # such thing as a duplicate option).
            if 'An error occured. An entry with that name already exists.' == str(e):
                return render_template('option_add.html', form=form, already_entered=True)
            else:
                flash(str(e), 'error')
                return render_template('option_add.html', form=form, already_entered=False)
    return render_template('option_add.html', title='New Option', form=form, already_entered=False)


@app.route('/option')
def option():
    contract_id = request.args.get('contract_id')
    try:
        option = TemplateAPI.option(contract_id)
    except PermissionError:
        return render_template('error.html', error=PERMISSION_DENIED)
    return render_template('option.html', title='Option Details', option=option)


def check_error_number_of_contracts(num_contracts, contract_id, action):
    if num_contracts:
        if is_integer(num_contracts):
            return None
    option = TemplateAPI.option(contract_id)
    flash(f'You must provide the number of contracts to {action}.', 'error')
    return redirect(f'option?contract_id={contract_id}')


def option_redirect(contract_id):
    option = TemplateAPI.option(contract_id)
    return redirect(f'option?contract_id={contract_id}')


@app.route('/fund', methods=['POST'])
def fund():
    contract_id = request.form.get('contract_id')
    num_contracts = request.form.get('num_contracts_fund')
    # If num_contracts missing/isn't an int, flash error and render page:
    error_render = check_error_number_of_contracts(num_contracts, contract_id, 'fund')
    if error_render:
        return error_render
    # Try to fund the contract, return any errors or display success:
    result = TemplateAPI.fund(contract_id, int(num_contracts))
    if not (result.get('error') is None):
        flash(result.get('error'), 'error')
    else:
        flash(f'Funded {num_contracts} contract/s. Please wait for funding transaction to confirm to see updated Liquidity.', 'success')
    return option_redirect(contract_id)


@app.route('/cancel', methods=['POST'])
def cancel():
    contract_id = request.form.get('contract_id')
    num_contracts = request.form.get('num_contracts_cancel')
    error_render = check_error_number_of_contracts(num_contracts, contract_id, 'cancel')
    if error_render:
        return error_render
    result = TemplateAPI.cancel(contract_id, int(num_contracts))
    if not (result.get('error') is None):
        flash(result.get('error'), 'error')
    else:
        flash(f'Cancelled {num_contracts} contract/s. Please wait for cancel transaction to confirm to see updated Liquidity.', 'success')
    return option_redirect(contract_id)


@app.route('/expire', methods=['POST'])
def expire():
    contract_id = request.form.get('contract_id')
    num_contracts = request.form.get('num_contracts_expire')
    error_render = check_error_number_of_contracts(num_contracts, contract_id, 'expire')
    if error_render:
        return error_render
    result = TemplateAPI.expire(contract_id, int(num_contracts))
    if not (result.get('error') is None):
        flash(result.get('error'), 'error')
    else:
        flash(f'Expired {num_contracts} contract/s. Please wait for expire transaction to confirm to see updated Liquidity.', 'success')
    return option_redirect(contract_id)


@app.route('/exercise', methods=['POST'])
def exercise():
    contract_id  = request.form.get('contract_id')
    num_contracts  = request.form.get('num_contracts_exercise')
    error_render = check_error_number_of_contracts(num_contracts, contract_id, 'exercise')
    if error_render:
        return error_render
    result = TemplateAPI.exercise(contract_id, int(num_contracts))
    if not (result.get('error') is None):
        flash(result.get('error'), 'error')
    else:
        flash(f'Exercised {num_contracts} contract/s. Please wait for exercise transaction to confirm to see updated Liquidity.', 'success')
    return option_redirect(contract_id)


@app.route('/settle', methods=['POST'])
def settle():
    contract_id  = request.form.get('contract_id')
    num_contracts  = request.form.get('num_contracts_settle')
    error_render = check_error_number_of_contracts(num_contracts, contract_id, 'settle')
    if error_render:
        return error_render
    result = TemplateAPI.settle(contract_id, int(num_contracts))
    if not (result.get('error') is None):
        flash(result.get('error'), 'error')
    else:
        flash(f'Settled {num_contracts} contract/s.', 'success')
    return option_redirect(contract_id)


@app.route('/export', methods=['POST'])
def export():
    contract_id  = request.form.get('contract_id')
    result = TemplateAPI.export(contract_id)
    if not (result.get('error') is None):
        flash(result.get('error'), 'error')
    option = TemplateAPI.export(contract_id)
    option = json.dumps(option, sort_keys = True, indent = 4, separators = (',', ': '))
    return render_template('option_export.html', option=option, contract_id=contract_id)


@app.route('/remove', methods=['POST'])
def remove():
    contract_id = request.form.get('contract_id')
    result = TemplateAPI.remove(contract_id)
    # Bit awkward but result is currently either True or an error in JSON for
    # this call. Unsure what will return False as success is True and error
    # is error.
    if type(result) is not bool:
        if not (result.get('error') is None):
            flash(f'Could not remove contract with ID {contract_id}: {result.get("error")}', 'error')
    else:
        flash(f'Removed contract with ID {contract_id}.', 'success')
    options_list = TemplateAPI.list()
    return render_template('options_list.html', options_list=options_list)


@app.route('/option_import', methods=['GET', 'POST'])
def option_import():
    example_data = {
        "contract_size": 1010,
        "expiry": 1669717410,
        "start": 1669717405,
        "strike_price": 1000,
        "coll_asset": "4a75e0dffa7c677e3b18e5570f146cc8cffb201a4fac0e9f7e17ec3cb9082934",
        "settle_asset": "dca9f967e1cb9f82367f03663dde5e0150ed9b70a32e5aeed787997c7295b2e1",
        "crt_rt_prevout_txid": "009363bb0f5d41700cfd61410757000505e3e9cd82bb3804631f76708d0e5884",
        "crt_rt_prevout_vout": 0,
        "ort_rt_prevout_txid": "60b4afafbdde49b66293d8d1ed6b51b8a163a065c0c1c9cbfc2db2adb85e6fd8",
        "ort_rt_prevout_vout": 2
    }
    example_data = json.dumps(example_data, sort_keys = True, indent = 4, separators = (',', ': '))
    form = OptionImportDataForm(import_data=example_data)
    if form.validate_on_submit():
        data = json.loads(form.import_data.data)
        try:
            new_entry = TemplateAPI.import_option(data)
            if not (new_entry.get('error') is None):
                flash(new_entry.get('error'), 'error')
                return render_template('option_import.html', title='Import Option', form=form)
            contract_id = new_entry['contract_id']
            flash(f'Imported new contract with ID {contract_id}.', 'success')
            return redirect(url_for('options_list'))
        except ValueError as e:
            # This duplicate test isn't implemented in this example but if you
            # want to then implement in API layer (although there is likely no
            # such thing as a duplicate option).
            if 'An error occured. An entry with that name already exists.' == str(e):
                return render_template('option_import', form=form, already_entered=True)
            else:
                flash(str(e), 'error')
                return render_template('option_import.html', form=form)
    return render_template('option_import.html', form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error=PAGE_NOT_FOUND)


@app.errorhandler(500)
def page_not_found(e):
    return render_template('error.html', error=APPLICATION_ERROR)


def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()
