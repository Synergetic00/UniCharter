FORCE_UPDATE=true

if [ ! -e 'data/courses.json' ] || $FORCE_UPDATE ; then
    echo 'Downloaded courses json file'
    python scrapers/courses.py
fi

if [ ! -e 'data/units.json' ] || $FORCE_UPDATE ; then
    echo 'Downloaded unit json file'
    python scrapers/units.py
fi