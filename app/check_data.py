def check_observation_data(temperature, cloudiness, precipitation_amount, precipitation_type):
    errors = []

    # Tarkista, vain lämpötila-prametri voi olla tyhjä
    if cloudiness is None or precipitation_amount is None or precipitation_type is None:
        errors.append("Kaikille parametreille (paitsi lämpötila) on annettava arvo.")

    # Tarkista lämpötila
    if temperature is not None:
        if temperature < -60 or temperature > 50:
            errors.append("Lämpötila ei voi olla alle -60 tai yli +50 astetta.")

    # Tarkista pilvisyys ja sateen määrä
    if cloudiness == 0 and precipitation_amount != 0:
        errors.append("Sadetta ei voi olla ilman pilvisyyttä.")

    # Tarkista sateen määrä ja sateen olomuoto
    if precipitation_amount == 0 and precipitation_type != 0:
        errors.append("Sateella ei voi olla olomuotoa ilman sadetta.")

    return errors