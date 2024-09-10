from flask import Flask, render_template, jsonify,request
app= Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')
# This endpoint calculates the required SIP (Systematic Investment Plan) amount needed to achieve a target value given an annual rate of return and a specified investment duration in years.
@app.route('/api/investment/sip/required',methods=['GET'])
def required():
    target_value = float(request.args.get('target_value'))
    annual_rate_of_return = float(request.args.get('annual_rate_of_return'))
    years = int(request.args.get('years'))

    rate = float(annual_rate_of_return)/100
    monthly_rate_of_return = rate / 12
    print('Monthly rate of return',monthly_rate_of_return)
    
    total_months = years * 12
    
    sip = target_value / (((1 + monthly_rate_of_return)**total_months - 1) / monthly_rate_of_return * (1 + monthly_rate_of_return));
    
    return jsonify({
        "target_value":target_value,
        "annual_rate_of_return":annual_rate_of_return,
        "years":years,
        "required_sip": round(sip,2)
    })

# This endpoint calculates the amount of withdrawals that can be made from an initial investment, given a withdrawal amount, withdrawal frequency, inflation rate, rate of return, and investment duration.
@app.route('/api/investment/swp/withdrawals',methods=['GET'])
def withdrawals():
    initial_investment = float(request.args.get('initial_investment'))
    withdrawal_amount = float(request.args.get('withdrawal_amount'))
    withdrawal_frequency = request.args.get('withdrawal_frequency')  # "annually" assumed for simplicity
    num_withdrawals = int(request.args.get('num_withdrawals'))
    inflation_rate = float(request.args.get('inflation_rate'))
    roi = float(request.args.get('roi'))
    

    investment = initial_investment
    results = []

    for withdrawal_num in range(1, num_withdrawals + 1):
        investment_growth = investment * roi
        
        results.append({
            "current_investment": round(investment, 2),
            "investment_growth": round(investment_growth, 2),
            "withdrawal": withdrawal_num,
            "withdrawal_per_period": round(withdrawal_amount, 2)
        })
        
        investment = investment + investment_growth - withdrawal_amount
        withdrawal_amount += withdrawal_amount * inflation_rate


    return jsonify({
        "initial_investment": initial_investment,
        "withdrawal_amount": request.args.get('withdrawal_amount'),
        "withdrawal_frequency": withdrawal_frequency,
        "num_withdrawals": num_withdrawals,
        "inflation_rate": inflation_rate,
        "roi": roi,
        "results": results
    })
    
# This endpoint calculates the number of withdrawals that can be made from an initial investment, given a withdrawal amount, withdrawal frequency, inflation rate, and rate of return, before the investment is depleted.
@app.route('/api/withdrawals/swp/num_until_depleted', methods=['GET'] )
def num_until_depleted():
    initial_investment = float(request.args.get('initial_investment'))
    withdrawal_amount = float(request.args.get('withdrawal_amount'))
    withdrawal_frequency = str(request.args.get('withdrawal_frequency')) 
    inflation_rate = float(request.args.get('inflation_rate')) 
    roi = float(request.args.get('roi')) 
    
   
    investment = initial_investment
    withdrawals_made = 0

    if withdrawal_frequency == "monthly":
        withdrawals_per_year = 12
    elif withdrawal_frequency == "quarterly":
        withdrawals_per_year = 4
    else: 
        withdrawals_per_year = 1
    
    while investment > 0:
        if withdrawals_made > 0 and withdrawals_made % withdrawals_per_year == 0:
            withdrawal_amount += withdrawal_amount * inflation_rate
        
        investment -= withdrawal_amount
        
        if investment < 0:
            break
        
        investment += investment * (roi / withdrawals_per_year)
        
        withdrawals_made += 1

    return jsonify({
            "initial_investment": initial_investment,
            "withdrawal_amount": withdrawal_amount,
            "withdrawal_frequency": withdrawal_frequency,
            "inflation_rate": inflation_rate,
            "roi": roi,
            "num_withdrawals_until_depleted": withdrawals_made
        })


# This endpoint calculates the total amount of money that can be withdrawn from an initial investment, given a withdrawal amount, withdrawal frequency, inflation rate, rate of return, and investment duration.
@app.route('/api/withdrawals/swp/total_withdrawn', methods=['GET'])
def total_withdrawn():
    initial_investment = float(request.args.get('initial_investment'))
    withdrawal_amount = float(request.args.get('withdrawal_amount'))
    withdrawal_frequency = request.args.get('withdrawal_frequency')  
    inflation_rate = float(request.args.get('inflation_rate')) 
    roi = float(request.args.get('roi')) 
    
  
    if withdrawal_frequency == "monthly":
        withdrawals_per_year = 12
    elif withdrawal_frequency == "quarterly":
        withdrawals_per_year = 4
    else:  
        withdrawals_per_year = 1
    
   
    investment = initial_investment
    total_amount_withdrawn = 0
    num_withdrawals = 0
    

    while investment > 0:
       
        investment_growth = investment * (roi / withdrawals_per_year)
        investment += investment_growth
        
        
        investment -= withdrawal_amount
        total_amount_withdrawn += withdrawal_amount
        num_withdrawals += 1
        
     
        withdrawal_amount += withdrawal_amount * (inflation_rate / withdrawals_per_year)
        
       
        if investment <= 0:
            break


        return jsonify({
        "initial_investment": initial_investment,
        "withdrawal_amount": float(request.args.get('withdrawal_amount')),
        "withdrawal_frequency": withdrawal_frequency,
        "inflation_rate": inflation_rate,
        "roi": roi,
        "num_withdrawals": num_withdrawals,
        "total_amount_withdrawn": round(total_amount_withdrawn, 2),
        "withdrawals_per_year": withdrawals_per_year
    })
    



if __name__ == '__main__':
    app.run(debug=True)