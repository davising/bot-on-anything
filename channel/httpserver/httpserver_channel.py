from channel.channel import Channel
from config import channel_conf
from common import const
from flask import Flask, request, jsonify
from urllib.parse import parse_qs
from common.log import logger

app = Flask(__name__)

class HttpServerChannel(Channel):
    def startup(self):
        app.config['JSON_AS_ASCII'] = False
        hostName = channel_conf(const.HTTPSERVER).get('host')
        serverPort = channel_conf(const.HTTPSERVER).get('port')
        app.run(hostName, serverPort, debug=False)

@app.route('/api/openai', methods=['POST'])
def process_submit():
    req_params_path = "query=" + request.form["query"] + "&from_user_id=" + request.form["from_user_id"]
    req_decode_params = parse_qs(req_params_path)
    logger.info(req_decode_params)
    query = ""
    from_user_id = ""
    if 'query' in req_decode_params:
        query = req_decode_params['query'][0]

    if 'from_user_id' in req_decode_params:
        from_user_id = req_decode_params['from_user_id'][0]

    if query == "" or query.isspace() or from_user_id == "" or from_user_id.isspace():
        return jsonify({"data":""})

    result = ""
    context = {"from_user_id": from_user_id}
    for res in Channel().build_reply_content(query, context):
        result = result + "" + res

    response = {
        "data": result
    }

    # Encode the response data as a JSON string
    return jsonify(response)