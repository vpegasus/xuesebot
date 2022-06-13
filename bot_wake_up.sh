echo "rasa 启动中..."
nohup rasa run --enable-api >> ./cache/run_log/rasa.log 2>&1 &
echo "rasa actions 启动中..."
nohup rasa run actions >> ./cache/run_log/action.log 2>&1 &
echo "tts 启动中..."
nohup paddlespeech_server start --config_file ./conf/tts_online_application.yaml >> ./cache/run_log/tts.log 2>&1 &
echo "asr 启动中..."
nohup paddlespeech_server start --config_file conf/ws_conformer_application.yaml >> ./cache/run_log/asr.log 2>&1 &
nohup paddlespeech_server start --config_file conf/punc_application.yaml >> ./cache/run_log/punc.log 2>&1 &

sleep 20s
python interact.py