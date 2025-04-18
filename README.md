# My Apprentice

# Installation 

```
pip install pip-tools
pip-compile requirements.in
pip install -r requirements.txt
```

## After installing new library via pip, please also run the followings to keep dependency up to date 
```
pip-chill > requirements.in
pip-compile requirements.in --output-file requirements.txt
```

# Run 

```
streamlit run src/home.py
```
