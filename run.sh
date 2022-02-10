FORCE_UPDATE=false

pyrun() {
    if [ "$(uname)" == "Darwin" ]; then
        python3 "scrapers/$1.py"
    else
        python "scrapers/$1.py"
    fi
}

if [ ! -e 'data/courses.json' ] || $FORCE_UPDATE ; then
    echo 'Downloaded courses json file'
    pyrun "courses"
fi

if [ ! -e 'data/units.json' ] || $FORCE_UPDATE ; then
    echo 'Downloaded unit json file'
    pyrun "units"
fi