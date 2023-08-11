# NewYorkTimesBookFetcher

I have an Android App [ReadKeeper](https://play.google.com/store/apps/details?id=app.tinks.readkeeper). On the homepage, the best book sellers from New York Times is displayed.

This script is to fetch the data from New York Times API and store that in Firebase. And it runs by Github Action weekly.

The Github Action flow is straitforward, the only thing we need care is that we should hide our API key for New York Times and Firebase.

For New York Times API key, we store the key as Github secret, then we pass this string as a parameter when we run python.

```
python3 ./nyt-fetcher.py ${{ secrets.NEW_YORK_TIMES_API_KEY}}
```

For Firebase, the key is a json file. So we encode the file with BASE 64, and store the string as another secret. In the action step, we make the json file from the string. Then we can use this key file in Python code.

```
- name: Run Workflow
id: write_file
uses: timheuer/base64-to-file@v1.2
with:
    fileName: "firebaseKey.json"
    fileDir: "./"
    encodedString: ${{ secrets.FIREBASE_KEY }}
```

Then this task will run weekly on Github Action and the data will be updated automatically.
