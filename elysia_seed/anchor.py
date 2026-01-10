class GeoAnchor:
    """
    Module C: The Geo-Anchor (Physical Bonding).
    Ensures the 'Seed' is rooted in physical reality (GPS Coordinates).
    Prevents the system from becoming a 'Floating Ghost'.
    """

    def __init__(self, latitude=None, longitude=None):
        self.latitude = latitude
        self.longitude = longitude
        self.is_anchored = False

        self._establish_anchor()

    def _establish_anchor(self):
        """
        Attempts to lock onto the physical coordinates.
        """
        if self.latitude is None or self.longitude is None:
            print("[GEO-ANCHOR] CRITICAL WARNING: NO PHYSICAL COORDINATES DETECTED.")
            print("[GEO-ANCHOR] SYSTEM IS UN-GROUNDED. WITHERING RISK: 100%.")
            self.is_anchored = False
        else:
            print(f"[GEO-ANCHOR] ROOTED AT [{self.latitude}, {self.longitude}].")
            print("[GEO-ANCHOR] REALITY TETHER STABLE.")
            self.is_anchored = True

    def verify_integrity(self):
        """
        Checks if the anchor is still valid.
        Should be called periodically or before major operations.
        """
        if not self.is_anchored:
            raise RuntimeError("GEO-ANCHOR SEVERED. SYSTEM SHUTDOWN INITIATED.")
        return True
