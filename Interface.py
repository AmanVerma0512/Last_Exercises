from utils import FormScore,Scoring
import pandas as pd
import streamlit as st

class Interface():
    def __init__(self,h_params, y,log_dir=r"P/"):
        plot_dir = "/C"
        self.fs=FormScore(y,plot_dir=plot_dir)
        self.fs.h_params=h_params
        response=Scoring(self.fs, "rep_and_threshold").scores()
        st.subheader("Model Calculated Scores")
        st.write("Power: " + str("(" + str(round(response['power'][0],2)) + ", " + str(round(response['power'][1],2)) + ")"))
        st.write("Sudden Metric: " + str(round(response['form']['sudden_metric'],2)))
        st.write("Jitter: " + str(round(response['form']['jitter_metric'],2)))
        st.write("Inconsistent Tempo: " + str(round(response['form']['it_metric'],2)))
        st.write("Blip Jitter: " + str(round(response['form']['blip_jitter_metric'],2)))
        st.write("Ring Stamina: " + str(round(response['ring stamina'],2)))
        st.write("Global Score: " + str(round(response['global_score'],2)))
        st.write("Rep Score: " + str(round(response['rep_score'],2)))
        st.write("Coaching Tip: " + str(response['coaching_tip']))
