FORCE_UPDATE=true

pyrun() {
    if [ "$(uname)" == "Darwin" ]; then
        python3 "$1.py"
    else
        python "$1.py"
    fi
}

if [ ! -e 'data/courses.json' ] || $FORCE_UPDATE ; then
    echo 'Downloaded courses json file'
    pyrun "scrapers/courses"
fi

if [ ! -e 'data/units.json' ] || $FORCE_UPDATE ; then
    echo 'Downloaded unit json file'
    pyrun "scrapers/units"
fi

if [ ! -e 'data/prereqs.json' ] || $FORCE_UPDATE ; then
    echo 'Parsed unit for prerequisites'
    pyrun "parsers/prereqs"
fi