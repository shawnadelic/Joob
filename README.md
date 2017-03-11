Joob Song Lyric Analyzer and Generator
--------------------------------------

Installation:

1. Clone a local repository

2. Create a virtualenv

        virtualenv -p python3 venv

3. Activate the virtualenv

        source venv/bin/activate

4. Use pip to install application

        pip install -e.[dev]
        pip install -e.[testing]

5. Once installed, run command to build rhyme dictionary

        build_dict

6. The following command generates a song

        generate_song output.txt

7. The following command trains on data

        train path/to/data

8. The following command runs the tests (requires test.db
   to be generated in main directory).

        python setup.py test
