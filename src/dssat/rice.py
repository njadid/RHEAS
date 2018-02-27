""" Class definition for the DSSAT rice interface

.. module:: dssat
   :synopsis: Definition of the DSSAT rice class

.. moduleauthor:: Kostas Andreadis <kandread@jpl.nasa.gov>

"""

from dssat import DSSAT
from datetime import timedelta
import rpath
import logging
import subprocess
import os
import dbio


class Model(DSSAT):

    def _writeFileNames(self, fout, ens):
        """Write file name section in DSSAT control file."""
        fout.write("*MODEL INPUT FILE            B     1     1     5   999     0\r\n")
        fout.write("*FILES\r\n")
        fout.write("MODEL          RICER040\r\n")
        fout.write("FILEX          IRMZ8601.RIX\r\n")
        fout.write("FILEA          IRMZ8601.RIA\r\n")
        fout.write("FILET          IRMZ8601.RIT\r\n")
        fout.write("SPECIES        RICER040.SPE\r\n")
        fout.write("ECOTYPE        RICER040.ECO\r\n")
        fout.write("CULTIVAR       RICER040.CUL\r\n")
        fout.write("PESTS          RICER040.PST\r\n")
        fout.write("SOILS          SOIL.SOL\r\n")
        fout.write("WEATHER        WEATH{0:03d}.WTH\r\n".format(ens+1))
        fout.write("OUTPUT         OVERVIEW\r\n")

    def _writeSimulationControl(self, fout, startdate):
        """Write simulation control section in DSSAT control file."""
        fout.write("*SIMULATION CONTROL\r\n")
        fout.write("                   1     1     S {0}  2150 IRRI MUNOZ JAN 86 UREASE  RICER\r\n".format(startdate.strftime("%Y%j")))
        fout.write("                   Y     Y     N     N     N     N     N     N\r\n")
        fout.write("                   M     M     E     R     S     C     R     1     G\r\n")
        fout.write("                   R     R     R     R     M\r\n")
        fout.write("                   N     Y     Y     1     Y     N     Y     Y     N     N     Y     N     N\r\n")

    def _writeAutomaticMgmt(self, fout, startdate):
        """Write automatic management section in DSSAT control file."""
        t0 = startdate - timedelta(3)
        t1 = t0 + timedelta(14)
        fout.write("!AUTOMATIC MANAGEM\r\n")
        fout.write("               {0} {1}   40.  100.   30.   40.   10.\r\n".format(t0.strftime("%Y%j"), t1.strftime("%Y%j")))
        fout.write("                 30.   50.  100. IB001 IB001  10.0 1.000\r\n")
        fout.write("                 30.   50.   25. IB001 IB001\r\n")
        fout.write("                100.     1   20.\r\n")
        fout.write("                     0 1986036  100.    0.\r\n")

    def _writeExpDetails(self, fout):
        """Write experiment details section in DSSAT control file."""
        fout.write("*EXP.DETAILS\r\n")
        fout.write("  1IRMZ8601 RI IRRI,MUNOZ JAN 86 UREASE INHIBITORS\r\n")

    def _writeTreatments(self, fout):
        """Write treatments section in DSSAT control file."""
        fout.write("*TREATMENTS\r\n")
        fout.write("  5 1 0 0 140 kg N as urea(2/3 18 D\r\n")

    def _writeCultivars(self, fout):
        """Write cultivars section in DSSAT control file."""
        fout.write("*CULTIVARS\r\n")
        fout.write("   RI IB0012 IR 58\r\n")

    def _writeFields(self, fout, lat, lon):
        """Write fields section in DSSAT control file."""
        fout.write("*FIELDS\r\n")
        fout.write("   IRMZ0001 IRMZ8601   0.0    0. IB000    0.  100. 00000         50. IBRI910002\r\n")
        fout.write("           0.00000         0.00000      0.00               1.0  100.   1.0   0.0\r\n")

    def _writeInitialConditions(self, fout, startdate, dz, smi):
        """Write initial condition section in DSSAT control file."""
        fout.write("*INITIAL CONDITIONS\r\n")
        fout.write("   RI    {0}  600.    0.  1.00  1.00   0.0   800  1.10  0.00  100.   15.\r\n".format(startdate.strftime("%Y%j")))
        for lyr in range(len(dz)):
            fout.write("{0:8.0f}{1:8.3f}{2:8.1f}{3:8.1f}\r\n".format(dz[lyr], smi[0, lyr], 0.5, 0.1))

    def _writePlanting(self, fout, pdt):
        """Write planting details section in DSSAT control file."""
        fout.write("*PLANTING DETAILS\r\n")
        fout.write("   {0}     -99  75.0  25.0     T     H   20.    0.   2.0    0.   23.  26.0   3.0   0.0\r\n".format(pdt.strftime("%Y%j")))

    def _writeIrrigation(self, fout, irrigation):
        """Write irrigation details section in DSSAT control file."""
        fout.write("*IRRIGATION\r\n")
        fout.write("   1.000   30.   75.  -99. GS000 IR001   1.0\r\n")
        for i, irrig in enumerate(irrigation):
            fout.write("   {0} IR{1:03d} {2:4.1f}\r\n".format(irrig[0].strftime("%Y%j"), i+1, irrig[1]))

    def _writeFertilizer(self, fout, fertilizers):
        """Write fertilizer section in DSSAT control file."""
        fout.write("*FERTILIZERS\r\n")
        for f, fert in enumerate(fertilizers):
            dt, amount, percent = fert
            fout.write("   {0} FE{1:03d} AP{1:03d}   {2:02d}.   {3:02d}.    0.    0.    0.    0.   -99\r\n".format(dt.strftime("%Y%j"), f+1, amount, percent))

    def _writeResidues(self, fout):
        """Write residues section in DSSAT control file."""
        fout.write("*RESIDUES\r\n")

    def _writeChemicals(self, fout):
        """Write chemicals section in DSSAT control file."""
        fout.write("*CHEMICALS\r\n")

    def _writeTillage(self, fout):
        """Write tillage section in DSSAT control file."""
        fout.write("*TILLAGE\r\n")

    def _writeEnvironment(self, fout):
        """Write environment section in DSSAT control file."""
        fout.write("*ENVIRONMENT\r\n")

    def _writeHarvest(self, fout):
        """Write chemicals section in DSSAT control file."""
        fout.write("*HARVEST\r\n")

    def _writeSoil(self, fout, prof, dz):
        """Write soil section in DSSAT control file."""
        fout.write("*SOIL\r\n")
        for ln in prof[:-1]:
            fout.write(ln+"\r\n")
        fout.write("\r\n")
        for z in dz:
            fout.write("{0:6.0f}   0.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0\r\n".format(z))

    def _writeCultivar(self, fout, cultivar):
        """Write cultivar information in DSSAT control file."""
        fout.write("*CULTIVAR\r\n")
        fout.write(cultivar)

    def cultivar(self, ens, gid):
        """Retrieve Cultivar parameters for pixel and ensemble member."""
        db = dbio.connect(self.dbname)
        cur = db.cursor()
        sql = "select p1,p2r,p5,p2o,g1,g2,g3,g4,name from dssat.cultivars as c,{0}.agareas as a where crop='rice' and ensemble={1} and st_intersects(c.geom,a.geom) and a.gid={2}".format(self.name, ens + 1, gid)
        cur.execute(sql)
        if not bool(cur.rowcount):
            sql = "select p1,p2r,p5,p2o,g1,g2,g3,g4,name from dssat.cultivars as c,{0}.agareas as a where crop='rice' and ensemble={1} and a.gid={2} order by st_centroid(c.geom) <-> st_centroid(a.geom)".format(self.name, ens + 1, gid)
            cur.execute(sql)
        p1, p2r, p5, p2o, g1, g2, g3, g4, cname = cur.fetchone()
        # FIXME: Should the name of the cultivar be reflected in the line below?
        cultivar = "IB0012 IR 58            IB0001{0:6.1f}{1:6.1f}{2:6.1f}{3:6.1f}{4:6.1f}{5:6.4f}{6:6.2f}{7:6.2f}".format(p1, p2r, p5, p2o, g1, g2, g3, g4)
        cur.close()
        db.close()
        self.cultivars[gid].append(cname)
        return cultivar

    def writeControlFile(self, modelpath, vsm, depths, startdate, gid, lat, lon, planting, fertilizers, irrigation):
        """Writes DSSAT control file for specific pixel."""
        startdate = startdate.replace(2009)  # Temporary fix for weird DSSAT bug that crashes when year is after 2010
        planting = planting.replace(2009)
        if isinstance(vsm, list):
            vsm = (vsm * (int(self.nens / len(vsm)) + 1))[:self.nens]
        else:
            vsm = [vsm] * self.nens
        profiles = self.sampleSoilProfiles(gid)
        profiles = [p[0] for p in profiles]
        self.cultivars[gid] = []
        for ens in range(self.nens):
            sm = vsm[ens]
            fertilizers = [(startdate, 30, 20)] if fertilizers is None else fertilizers
            irrigation = [(startdate, 0.0)] if irrigation is None else irrigation
            prof = profiles[ens].split("\r\n")
            dz = map(lambda ln: float(ln.split()[0]), profiles[ens].split("\n")[3:-1])
            smi = self.interpolateSoilMoist(sm, depths, dz)
            cultivar = self.cultivar(ens, gid)
            filename = "{0}/DSSAT{1}_{2:03d}.INP" .format(modelpath, self.nens, ens + 1)
            with open(filename, 'w') as fout:
                self._writeFileNames(fout, ens)
                self._writeSimulationControl(fout, startdate)
                self._writeAutomaticMgmt(fout, startdate)
                self._writeExpDetails(fout)
                self._writeTreatments(fout)
                self._writeCultivars(fout)
                self._writeFields(fout, lat, lon)
                self._writeInitialConditions(fout, startdate, dz, smi)
                self._writePlanting(fout, planting)
                self._writeIrrigation(fout, irrigation)
                self._writeFertilizer(fout, fertilizers)
                self._writeResidues(fout)
                self._writeChemicals(fout)
                self._writeTillage(fout)
                self._writeEnvironment(fout)
                self._writeHarvest(fout)
                self._writeSoil(fout, prof, dz)
                self._writeCultivar(fout, cultivar)
        return dz, smi

    def run(self):
        "Override executable for DSSAT rice model."
        dssatexe = "{0}/DSSAT_Ex.exe".format(rpath.bins)
        return super(Model, self).run(exe=dssatexe)

    def setupModelInstance(self, geom, dssatexe):
        """Overrides setting up parameters and writing input files for a DSSAT model instance
        over a specific geometry."""
        return super(Model, self).setupModelInstance(geom, "DSSAT_Ex.exe")

    def runModelInstance(self, modelpath, dssatexe):
        """Override run function of DSSAT model instance."""
        log = logging.getLogger(__name__)
        dssatexe = "DSSAT_Ex.exe"
        os.chdir(modelpath)
        for ens in range(self.nens):
            proc = subprocess.Popen(["wine", dssatexe, "D", "DSSAT{0}_{1:03d}.INP".format(self.nens, ens+1)])
            out, err = proc.communicate()
            log.debug(out)
            os.rename("PlantGro.OUT", "PLANTGRO{0:03d}.OUT".format(ens+1))

    def writeWeatherFiles(self, modelpath, name, year, month, day, weather, elev, lat, lon, ts=None, te=None):
        """Overrides writing ensemble weather files for specific pixel."""
        return super(Model, self).writeWeatherFiles(modelpath, name, [2009]*len(month), month, day, weather, elev, lat, lon)

    def yieldTable(self):
        """Create table for crop yield statistics and crop type."""
        super(Model, self).yieldTable()
        db = dbio.connect(self.dbname)
        cur = db.cursor()
        sql = "update {0}.yield set crop='rice' where crop is null".format(self.name)
        cur.execute(sql)
        db.commit()
        cur.close()
        db.close()
