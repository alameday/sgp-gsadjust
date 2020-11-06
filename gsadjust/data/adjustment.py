"""
data/adjustment.py
===============

GSadjust objects for Adjustment | AdjustmentOptions | AdjustmentResults: The first contains
instances of the latter two. Holds the input data, options, and results of the
network adjustment.

This software is preliminary, provisional, and is subject to revision. It is
being provided to meet the need for timely best science. The software has not
received final approval by the U.S. Geological Survey (USGS). No warranty,
expressed or implied, is made by the USGS or the U.S. Government as to the
functionality of the software and related material nor shall the fact of release
constitute any such warranty. The software is provided on the condition tha
neither the USGS nor the U.S. Government shall be held liable for any damages
resulting from the authorized or unauthorized use of the software.
"""
import numpy as np


class AdjustmentResults:
    """
    Object to store least-squares adjustment statistics.
    """

    def __init__(self):
        self.n_deltas, self.n_deltas_notused = 0, 0
        self.n_datums, self.n_datums_notused = 0, 0
        self.n_unknowns = 0
        self.max_dg_residual, self.min_dg_residual = 0, 0
        self.max_datum_residual, self.min_datum_residual = 0, 0
        self.avg_stdev = 0
        self.chi2, self.chi2c = 0, 0
        self.cal_dic, self.netadj_drift_dic = {}, {}
        self.text = []

    def __str__(self):
        return_str = ''
        for attr in vars(self):
            if attr != 'text':
                return_str += '{}: {}\n'.format(attr, getattr(self, attr))
        for line in self.text:
            return_str += line
        return return_str

    def get_report(self):
        chi_result = "accepted" if self.chi2 < self.chi2c else "rejected"
        text = [
            f"Number of unknowns:                  {self.n_unknowns:d}",
            f"Number of relative observations:     {self.n_deltas:d}",
            f"Number of absolute observations:     {self.n_datums:d}",
            f"Degrees of freedom (nobs-nunknowns): {self.dof:d}",
            f"SD a posteriori:                     {self.chi2 / self.dof:4f}",
            f"chi square value:                  {self.chi2:6.2f}",
            f"critical chi square value:         {self.chi2c:6.2f}",
            f"Chi-test {chi_result}",
            f"Average standard deviation:          {self.avg_stdev:.2f}",
            f"Maximum delta residual:              {self.max_dg_residual:.2f}",
            f"Maximum absolute datum residual:     {self.max_datum_residual:.2f}",
            f"Minimum absolute datum residual:     {self.min_datum_residual:.2f}",
        ]

        return text


class AdjustedStation:
    """
    Object to store the network-adjusted gravity value at each station.
    """

    def __init__(self, station, g, sd):
        self.station = station
        self.g = g
        self.sd = sd

    def __str__(self):
        return '{} {:0.2f} {:0.2f}'.format(self.station, self.g, self.sd)


class AdjustmentOptions:
    """
    Object that holds options for least-squares adjustment.

    Options are set by gui.dialogs.AdjustOptions().
    """

    def __init__(self):
        # self.use_model_temp = False
        # self.model_temp_degree = 0
        self.use_sigma_prefactor = False
        self.sigma_prefactor = 1.0
        self.use_sigma_postfactor = False
        self.sigma_postfactor = 1.0
        self.use_sigma_add = False
        self.sigma_add = 0.0
        self.use_sigma_min = False
        self.sigma_min = 3.0
        self.alpha = 0.05
        self.cal_coeff = False
        self.adj_type = 'gravnet'
        self.specify_cal_coeff = False
        self.meter_cal_dict = None

    def __str__(self):
        return_str = ''
        for attr in vars(self):
            return_str += '{}: {}\n'.format(attr, getattr(self, attr))
        return return_str


class Adjustment:
    """
    Object that holds least-squares adjustment input matrices and results.

    There is one Adjustment object per Survey.

    Attributes
    __________
    A : ndarray
        model matrix (Nobs rel + NobsAbs)*Nunknowns
    P : ndarray
        Weight matrix (Nobs rel + NobsAbs)*(Nobs rel + NobsAbs)
    Obs                 observation vector (Nobs rel + NobsAbs)
    S                   StX=0
    X                   Unknowns
    r                   residuals (V)
    var                 Diagonal of the a posteriori covariance matrix
    VtPV
    dof                 degree of freedom (Nobs rel + NobsAbs - Nunknowns)
    """

    def __init__(self):
        """
        Initializes

        """
        self.A = np.array([])
        self.P = np.array([])
        self.Obs = np.array([])
        self.S = np.array([])
        self.X = np.array([])
        self.r = np.array([])
        self.var = np.array([])
        self.VtPV = np.array([])
        self.SDaposteriori = 0
        self.dof = 0
        self.n_meters = 0
        self.meter_dic = dict()
        self.deltas = []
        self.datums = []
        self.g_dic = dict()
        self.sd_dic = dict()
        self.netadj_loop_keys = dict()
        self.sta_dic_ls = dict()
        self.adjustmentoptions = AdjustmentOptions()
        self.adjustmentresults = AdjustmentResults()

    def results_string(self):
        try:
            if self.adjustmentresults.text:  # Gravnet results
                return [x + '\n' for x in self.adjustmentresults.text]
            elif self.adjustmentresults.n_unknowns > 0:
                # text_out.append("Number of stations:                 {:d}\n".format(len(sta_dic_ls)))
                # text_out.append("Number of loops:                    {:d}\n".format(nloops))
                # text_out.append("Polynomial degree for time:         {:d}\n".format(drift_time))
                text_out = self.adjustmentresults.get_report()
                if self.adjustmentoptions.cal_coeff:
                    for k, v in self.adjustmentresults.cal_dic.items():
                        text_out.append(
                            "Calibration coefficient for meter {}: {:.6f} +/- {:.6f}".format(
                                k, v[0], v[1]
                            )
                        )
                elif self.adjustmentoptions.specify_cal_coeff:
                    for k, v in self.adjustmentresults.meter_cal_dict.items():
                        text_out.append(
                            "Specified calibration coefficient for meter {}: {:.6f}".format(
                                k, v
                            )
                        )
                if self.netadj_loop_keys:
                    text_out.append("Network adjustment drift coefficient(s):")
                    for loop in self.netadj_loop_keys.items():
                        # this dict only has loops with netadj option
                        text_out.append("Loop " + loop[0] + ": ")
                        for i in range(loop[1][1]):
                            # degree of polynomial
                            degree = self.X[
                                len(self.sta_dic_ls) + self.n_meters + loop[1][0] + i
                            ][0]
                            if degree == 1:
                                text_out.append(
                                    "Drift coefficient, degree {}: {:.3f}".format(
                                        i + 1, degree
                                    )
                                )
                            else:
                                text_out.append(
                                    "Drift coefficient, degree {}: {:.3f} (µGal/day)".format(
                                        i + 1, degree
                                    )
                                )
                return text_out
        except (AttributeError, TypeError):
            return ''

    @property
    def adjustment_gdic_str(self):
        return_str = ''
        for k, v in self.g_dic.items():
            return_str += '{} {:0.2f} {:0.2f}\n'.format(k, v, self.sd_dic[k])
        return return_str

    def python_lsq_inversion(self):
        """
        Solve system of equations using numpy linalg.inv. Similar to LSQ
        inversion from Hwang et al (2002)
        """
        At = np.transpose(self.A)
        # St = np.transpose(self.S)
        N = At.dot(self.P).dot(self.A)
        # original PyGrav solution:
        # self.X = np.linalg.inv(N+self.S.dot(St)).dot(At).dot(self.P).dot(self.Obs)
        self.X = np.linalg.inv(N).dot(At).dot(self.P).dot(self.Obs)
        self.r = self.A.dot(self.X) - self.Obs
        rt = np.transpose(self.r)
        self.VtPV = rt.dot(self.P).dot(self.r)
        var_post_norm = self.VtPV / self.dof
        self.SDaposteriori = np.sqrt(var_post_norm)
        cov_post = np.linalg.inv(N) * var_post_norm
        self.var = np.diagonal(cov_post)

    def lsq_statistics(self):
        """
        a priori variance of unit weight = 1
        """
        alpha = self.adjustmentoptions.alpha
        self.adjustmentresults.chi2 = self.VtPV[0][0]
        self.adjustmentresults.dof = self.dof
        t = np.sqrt(2 * np.log(1 / alpha))
        chi_1_alpha = t - (2.515517 + 0.802853 * t + 0.010328 * t ** 2) / (
            1 + 1.432788 * t + 0.189269 * t ** 2 + 0.001308 * t ** 3
        )
        dof = float(self.dof)
        self.adjustmentresults.chi2c = (
            dof * (chi_1_alpha * np.sqrt(2 / (9 * dof)) + 1 - 2.0 / (9 * dof)) ** 3
        )
