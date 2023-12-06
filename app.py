'''
App to score the predicted output
'''
import gradio as gr
import pandas as pd
import urllib.request
import json
import os
import ssl

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

def call_api(actualshippingdays, expectedshippingdays,
             carrier, yshippingdistance, xshippingdistance,
             inbulkorder, shippingorigin, orderdate,
             shippingpriority, ontimedelivery, computerbrand,
             computermodel, screensize, packageweight,
             url='http://3f6cc858-fb27-44a5-bd5c-5166cdabc429.canadaeast.azurecontainer.io/score'):
    # Replace this with the primary/secondary key or AMLToken for the endpoint
    api_key = os. getenv('AZURE_API_KEY')
    if not api_key:
        raise Exception("A key should be provided to invoke the endpoint")

    data = {
        "Inputs": {
            "input1": [
                {
                    "ActualShippingDays": actualshippingdays,
                    "ExpectedShippingDays": expectedshippingdays,
                    "OrderID": None,
                    "ProductId_R": None,
                    "ProductId": None,
                    "Carrier": carrier,
                    "YShippingDistance": yshippingdistance,
                    "XShippingDistance": xshippingdistance,
                    "InBulkOrder": inbulkorder,
                    "ShippingOrigin": shippingorigin,
                    "OrderDate": orderdate,
                    "ShippingPriority": shippingpriority,
                    "OnTimeDelivery": ontimedelivery,
                    "ComputerBrand": computerbrand,
                    "ComputerModel": computermodel,
                    "ScreenSize": screensize,
                    "PackageWeight": packageweight,
                }
            ]
        },
        "GlobalParameters": {}
    }
    body = str.encode(json.dumps(data))

    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)

        result = response.read()
        parsed_result = json.loads(result.decode('utf-8'))
        parsed_result = parsed_result["Results"]["WebServiceOutput0"][0]
        predicted_shipping_days = parsed_result["Scored Labels"]
        return predicted_shipping_days
    
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(error.read().decode("utf8", 'ignore'))

    
if __name__ == "__main__":
    allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.create_unverified_context', None):
    demo = gr.Interface(fn=call_api, 
                        inputs=[
                            gr.Number(label='Actual Shipping Days'),
                            gr.Number(label='Expected Shipping Days'),
                            gr.Dropdown(['GlobalFreight', 'MicroCarrier', 'Shipper', 'BigBird'], label='Carrier'),
                            gr.Number(label='YShippingDistance'),
                            gr.Number(label='XShippingDistance'),
                            gr.Dropdown(['Bulk Order', 'Single Order'], label='InBulkOrder'),
                            gr.Dropdown(['Atlanta', 'Seattle', 'Chicago', 'San Francisco', 'Las Vegas', 'Salt Lake City',
                                                'New York City', 'Houston'], label='ShippingOrigin'),
                            gr.Textbox(label='OrderDate, enter in form yyyy-mm-dd 00:00:00'),
                            gr.Dropdown(['Express', 'Standard', 'Ground', 'Air'], label='ShippingPriority'),
                            gr.Dropdown(['On Time', 'Late'], label='OnTimeDelivery'),
                            gr.Dropdown(['Bell', 'Howell', 'MicroChip', 'Orange'], label='ComputerBrand'),
                            gr.Dropdown(['Base', 'Performance', 'Standard'], label='ComputerModel'),
                            gr.Number(label='ScreenSize', minimum=10, maximum=19),
                            gr.Number(label='PackageWeight', minimum=4, maximum=9)
                        ], 
                        outputs="text",
                        live=True)
            
    demo.launch(show_api=False)   