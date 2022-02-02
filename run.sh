FORCE_UPDATE=false

if [ ! -e 'data/courses.json' ] || $FORCE_UPDATE ; then
    echo 'Downloaded courses json file'
    python scraper/courses.py
fi

if [ ! -e 'data/units.json' ] || $FORCE_UPDATE ; then
    echo 'Downloaded unit json file'
    python scraper/units.py
fi