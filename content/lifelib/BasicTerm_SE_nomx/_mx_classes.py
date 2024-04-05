from . import _mx_sys


class _c_Projection(_mx_sys.BaseSpace):

    def __init__(self, parent):

        # modelx variables
        self._space = self
        self._parent = parent
        self._model = parent._model


        self._mx_spaces = {

        }

        self._mx_itemspaces = {}
        self._mx_roots = []     # Dynamic Space only

        # Cache variables
        self._v_age = {}
        self._v_age_at_entry = None
        self._has_age_at_entry = False
        self._v_check_pv_net_cf = None
        self._has_check_pv_net_cf = False
        self._v_claim_pp = {}
        self._v_claims = {}
        self._v_commissions = {}
        self._v_disc_factors = None
        self._has_disc_factors = False
        self._v_disc_rate_mth = None
        self._has_disc_rate_mth = False
        self._v_duration = {}
        self._v_duration_mth = {}
        self._v_expense_acq = None
        self._has_expense_acq = False
        self._v_expense_maint = None
        self._has_expense_maint = False
        self._v_expenses = {}
        self._v_inflation_factor = {}
        self._v_inflation_rate = None
        self._has_inflation_rate = False
        self._v_lapse_rate = {}
        self._v_loading_prem = None
        self._has_loading_prem = False
        self._v_model_point = None
        self._has_model_point = False
        self._v_mort_rate = {}
        self._v_mort_rate_mth = {}
        self._v_net_cf = {}
        self._v_net_premium_pp = None
        self._has_net_premium_pp = False
        self._v_policy_term = None
        self._has_policy_term = False
        self._v_pols_death = {}
        self._v_pols_if = {}
        self._v_pols_if_at = {}
        self._v_pols_if_init = None
        self._has_pols_if_init = False
        self._v_pols_lapse = {}
        self._v_pols_maturity = {}
        self._v_pols_new_biz = {}
        self._v_premium_pp = None
        self._has_premium_pp = False
        self._v_premiums = {}
        self._v_proj_len = None
        self._has_proj_len = False
        self._v_pv_claims = None
        self._has_pv_claims = False
        self._v_pv_commissions = None
        self._has_pv_commissions = False
        self._v_pv_expenses = None
        self._has_pv_expenses = False
        self._v_pv_net_cf = None
        self._has_pv_net_cf = False
        self._v_pv_pols_if = None
        self._has_pv_pols_if = False
        self._v_pv_premiums = None
        self._has_pv_premiums = False
        self._v_result_cf = None
        self._has_result_cf = False
        self._v_result_pols = None
        self._has_result_pols = False
        self._v_result_pv = None
        self._has_result_pv = False
        self._v_sex = None
        self._has_sex = False
        self._v_sum_assured = None
        self._has_sum_assured = False

    def _mx_assign_refs(self, io_data, pickle_data):

        # Reference assignment
        self.disc_rate_ann = io_data[135534285205472]
        self.model_point_table = io_data[135534275327504]
        self.mort_table = io_data[135534200499616]
        self.np = _mx_sys.import_module('numpy')
        self.pd = _mx_sys.import_module('pandas')
        self.point_id = 1
        self.premium_table = io_data[135534283701696]

    def _mx_copy_refs(self, base, base_root):

        # Reference assignment
        self.disc_rate_ann = base.disc_rate_ann
        self.model_point_table = base.model_point_table
        self.mort_table = base.mort_table
        self.np = base.np
        self.pd = base.pd
        self.point_id = base.point_id
        self.premium_table = base.premium_table

    def _f_age(self, t):
        """The attained age at time t.

        Defined as::

            age_at_entry() + duration(t)

        .. seealso::

            * :func:`age_at_entry`
            * :func:`duration`

        """
        return self.age_at_entry() + self.duration(t)

    def _f_age_at_entry(self):
        """The age at entry of the selected model point

        The element labeled ``age_at_entry`` of the Series returned by
        :func:`model_point`.
        """
        return self.model_point()["age_at_entry"]

    def _f_check_pv_net_cf(self):
        """Check present value summation

        Check if the present value of :func:`net_cf` matches the
        sum of the present values each cashflows.
        Returns the check result as :obj:`True` or :obj:`False`.

         .. seealso::

            * :func:`net_cf`
            * :func:`pv_net_cf`

        """

        import math
        res = sum(list(self.net_cf(t) for t in range(self.proj_len())) * self.disc_factors()[:self.proj_len()])

        return math.isclose(res, self.pv_net_cf())

    def _f_claim_pp(self, t):
        """Claim per policy

        The claim amount per plicy. Defaults to :func:`sum_assured`.
        """
        return self.sum_assured()

    def _f_claims(self, t):
        """Claims

        Claims during the period from ``t`` to ``t+1`` defined as::

            claim_pp(t) * pols_death(t)

        .. seealso::

            * :func:`claim_pp`
            * :func:`pols_death`

        """
        return self.claim_pp(t) * self.pols_death(t)

    def _f_commissions(self, t): 
        """Commissions

        By default, 100% premiums for the first year, 0 otherwise.

        .. seealso::

            * :func:`premiums`
            * :func:`duration`

        """
        return self.premiums(t) if self.duration(t) == 0 else 0

    def _f_disc_factors(self):
        """Discount factors.

        Vector of the discount factors as a Numpy array. Used for calculating
        the present values of cashflows.

        .. seealso::

            :func:`disc_rate_mth`
        """
        return self.np.array(list((1 + self.disc_rate_mth()[t])**(-t) for t in range(self.proj_len())))

    def _f_disc_rate_mth(self):
        """Monthly discount rate

        Nummpy array of monthly discount rates from time 0 to :func:`proj_len` - 1
        defined as::

            (1 + disc_rate_ann)**(1/12) - 1

        .. seealso::

            :func:`disc_rate_ann`

        """
        return self.np.array(list((1 + self.disc_rate_ann[t//12])**(1/12) - 1 for t in range(self.proj_len())))

    def _f_duration(self, t):
        """Duration of the selected model point at ``t`` in years

        .. seealso:: :func:`duration_mth`

        """
        return self.duration_mth(t) // 12

    def _f_duration_mth(self, t):
        """Duration of the selected model point at ``t`` in months

        Indicates how many months the policies have been in-force at ``t``.
        The initial value at time 0 is read from the ``duration_mth`` column in
        :attr:`model_point_table` through :func:`model_point`.
        Increments by 1 as ``t`` increments.
        Negative values of :func:`duration_mth` indicate future new business
        policies. For example, If the :func:`duration_mth` is
        -15 at time 0, the model point is issued at ``t=15``.

        .. seealso:: :func:`model_point`

        """
        if t == 0:
            return self.model_point()['duration_mth']
        else:
            return self.duration_mth(t-1) + 1

    def _f_expense_acq(self):
        """Acquisition expense per policy

        ``300`` by default.
        """
        return 300

    def _f_expense_maint(self):
        """Annual maintenance expense per policy

        ``60`` by default.
        """
        return 60

    def _f_expenses(self, t):
        """Expenses

        Expenses during the period from ``t`` to ``t+1``
        defined as the sum of acquisition expenses and maintenance expenses.
        The acquisition expenses are modeled as :func:`expense_acq`
        times :func:`pols_new_biz`.
        The maintenance expenses are modeled as :func:`expense_maint`
        times :func:`inflation_factor` times :func:`pols_if_at` before
        decrement.

        .. seealso::

            * :func:`expense_acq`
            * :func:`expense_maint`
            * :func:`inflation_factor`
            * :func:`pols_new_biz`
            * :func:`pols_if_at`

        """

        return self.expense_acq() * self.pols_new_biz(t) \
            + self.pols_if_at(t, "BEF_DECR") * self.expense_maint()/12 * self.inflation_factor(t)

    def _f_inflation_factor(self, t):
        """The inflation factor at time t

        .. seealso::

            * :func:`inflation_rate`

        """
        return (1 + self.inflation_rate())**(t/12)

    def _f_inflation_rate(self):
        """Inflation rate"""
        return 0.01

    def _f_lapse_rate(self, t):
        """Lapse rate

        By default, the lapse rate assumption is defined by duration as::

            max(0.1 - 0.02 * duration(t), 0.02)

        .. seealso::

            :func:`duration`

        """
        return max(0.1 - 0.02 * self.duration(t), 0.02)

    def _f_loading_prem(self):
        """Loading per premium

        .. note::
           This cells is not used by default.

        ``0.5`` by default.

        .. seealso::

            * :func:`premium_pp`

        """
        return 0.50

    def _f_model_point(self):
        """The selected model point as a Series

        :func:`model_point` looks up :attr:`model_point_table`, and
        returns as a Series the row whose index is the value of
        :attr:`point_id`.

        Example:
            In the code below ``Projection`` refers to
            the :mod:`~basiclife.BasicTerm_SE.Projection` space::

                >>> Projection.point_id
                1

                >>> Projection.model_point()
                age_at_entry        47
                sex                  M
                policy_term         10
                policy_count        86
                sum_assured     622000
                duration_mth         1
                Name: 1, dtype: object

                >>> Projection.point_id = 2

                >>> Projection.model_point()
                age_at_entry        29
                sex                  M
                policy_term         20
                policy_count        56
                sum_assured     752000
                duration_mth       210
                Name: 2, dtype: object

        """
        return self.model_point_table.loc[self.point_id]

    def _f_mort_rate(self, t):
        """Mortality rate to be applied at time t

        .. seealso::

           * :attr:`mort_table`
           * :func:`mort_rate_mth`

        """
        return self.mort_table[str(max(min(5, self.duration(t)),0))][self.age(t)]

    def _f_mort_rate_mth(self, t):
        """Monthly mortality rate to be applied at time t

        .. seealso::

           * :attr:`mort_table`
           * :func:`mort_rate`

        """
        return 1-(1- self.mort_rate(t))**(1/12)

    def _f_net_cf(self, t):
        """Net cashflow

        Net cashflow for the period from ``t`` to ``t+1`` defined as::

            premiums(t) - claims(t) - expenses(t) - commissions(t)

        .. seealso::

            * :func:`premiums`
            * :func:`claims`
            * :func:`expenses`
            * :func:`commissions`

        """
        return self.premiums(t) - self.claims(t) - self.expenses(t) - self.commissions(t)

    def _f_net_premium_pp(self):
        """Net premium per policy

        .. note::
           This cells is not used by default.

        The net premium per policy is defined so that
        the present value of net premiums equates to the present value of
        claims::

            pv_claims() / pv_pols_if()

        .. seealso::

            * :func:`pv_claims`
            * :func:`pv_pols_if`

        """
        return self.pv_claims() / self.pv_pols_if()

    def _f_policy_term(self):
        """The policy term of the selected model point.

        The element labeled ``policy_term`` of the Series returned by
        :func:`model_point`.
        """

        return self.model_point()["policy_term"]

    def _f_pols_death(self, t):
        """Number of death occurring at time t"""
        return self.pols_if_at(t, "BEF_DECR") * self.mort_rate_mth(t)

    def _f_pols_if(self, t):
        """Number of policies in-force

        :func:`pols_if(t)<pols_if>` is an alias
        for :func:`pols_if_at(t, "BEF_MAT")<pols_if_at>`.

        .. seealso::
            * :func:`pols_if_at`

        """
        return self.pols_if_at(t, "BEF_MAT")

    def _f_pols_if_at(self, t, timing):
        """Number of policies in-force

        :func:`pols_if_at(t, timing)<pols_if_at>` calculates
        the number of policies in-force at time ``t``.
        The second parameter ``timing`` takes a string value to
        indicate the timing of in-force,
        which is either
        ``"BEF_MAT"``, ``"BEF_NB"`` or ``"BEF_DECR"``.

        .. rubric:: BEF_MAT

        The number of policies in-force before maturity after lapse and death.
        At time 0, the value is read from :func:`pols_if_init`.
        For time > 0, defined as::

            pols_if_at(t-1, "BEF_DECR") - pols_lapse(t-1) - pols_death(t-1)

        .. rubric:: BEF_NB

        The number of policies in-force before new business after maturity.
        Defined as::

            pols_if_at(t, "BEF_MAT") - pols_maturity(t)

        .. rubric:: BEF_DECR

        The number of policies in-force before lapse and death after new business.
        Defined as::

            pols_if_at(t, "BEF_NB") + pols_new_biz(t)

        .. seealso::
            * :func:`pols_if_init`
            * :func:`pols_lapse`
            * :func:`pols_death`
            * :func:`pols_maturity`
            * :func:`pols_new_biz`
            * :func:`pols_if`

        """
        if timing == "BEF_MAT":

            if t == 0:
                return self.pols_if_init()
            else:
                return self.pols_if_at(t-1, "BEF_DECR") - self.pols_lapse(t-1) - self.pols_death(t-1)

        elif timing == "BEF_NB":

            return self.pols_if_at(t, "BEF_MAT") - self.pols_maturity(t)

        elif timing == "BEF_DECR":

            return self.pols_if_at(t, "BEF_NB") + self.pols_new_biz(t)

        else:
            raise ValueError("invalid timing")

    def _f_pols_if_init(self): 
        """Initial number of policies in-force

        Number of in-force policies at time 0 referenced from
        :func:`pols_if_at(0, "BEF_MAT")<pols_if_at>`.
        """
        if self.duration_mth(0) > 0:
            return self.model_point()["policy_count"]
        else:
            return 0

    def _f_pols_lapse(self, t):
        """Number of lapse occurring at time t

        .. seealso::
            * :func:`pols_if_at`
            * :func:`lapse_rate`

        """
        return (self.pols_if_at(t, "BEF_DECR") - self.pols_death(t)) * (1-(1 - self.lapse_rate(t))**(1/12))

    def _f_pols_maturity(self, t):
        """Number of maturing policies

        The policy maturity occurs when
        :func:`duration_mth` equals 12 times :func:`policy_term`.
        The amount is equal to :func:`pols_if_at(t, "BEF_MAT")<pols_if_at>`.

        otherwise ``0``.
        """
        if self.duration_mth(t) == self.policy_term() * 12:
            return self.pols_if_at(t, "BEF_MAT")
        else:
            return 0

    def _f_pols_new_biz(self, t):
        """Number of new business policies

        The number of new business policies.
        The value :func:`duration_mth(0)<duration_mth>`
        for the selected model point is read from the ``policy_count`` column in
        :func:`model_point`. If the value is 0 or negative,
        the model point is new business at t=0 or at t when
        :func:`duration_mth(t)<duration_mth>` is 0, and the
        :func:`pols_new_biz(t)<pols_new_biz>` is read from the ``policy_count``
        in :func:`model_point`.

        .. seealso::
            * :func:`model_point`

        """
        if self.duration_mth(t) == 0:
            return self.model_point()['policy_count']
        else:
            return 0

    def _f_premium_pp(self):
        """Monthly premium per policy

        Monthly premium amount per policy defined as::

            round(sum_assured() * premium_table[age_at_entry(), policy_term()], 2)

        .. seealso::

            * :attr:`premium_table`
            * :func:`sum_assured`
            * :func:`age_at_entry`
            * :func:`policy_term`


        """
        return round(self.sum_assured() * self.premium_table[self.age_at_entry(), self.policy_term()], 2)

    def _f_premiums(self, t):
        """Premium income

        Premium income during the period from ``t`` to ``t+1`` defined as::

            premium_pp() * pols_if_at(t, "BEF_DECR")

        .. seealso::

            * :func:`premium_pp`
            * :func:`pols_if_at`

        """
        return self.premium_pp() * self.pols_if_at(t, "BEF_DECR")

    def _f_proj_len(self):
        """Projection length in months

        :func:`proj_len` indicates how many months the projection
        for the selected model point should be carried out. Defined as::

            12 * policy_term() - duration_mth(0) + 1

        .. seealso::

            :func:`policy_term`

        """
        return max(12 * self.policy_term() - self.duration_mth(0) + 1, 0)

    def _f_pv_claims(self):
        """Present value of claims

        .. seealso::

            * :func:`claims`

        """
        return sum(list(self.claims(t) for t in range(self.proj_len())) * self.disc_factors()[:self.proj_len()])

    def _f_pv_commissions(self):
        """Present value of commissions

        .. seealso::

            * :func:`expenses`

        """
        return sum(list(self.commissions(t) for t in range(self.proj_len())) * self.disc_factors()[:self.proj_len()])

    def _f_pv_expenses(self):
        """Present value of expenses

        .. seealso::

            * :func:`expenses`

        """
        return sum(list(self.expenses(t) for t in range(self.proj_len())) * self.disc_factors()[:self.proj_len()])

    def _f_pv_net_cf(self):
        """Present value of net cashflows.

        Defined as::

            pv_premiums() - pv_claims() - pv_expenses() - pv_commissions()

        .. seealso::

            * :func:`pv_premiums`
            * :func:`pv_claims`
            * :func:`pv_expenses`
            * :func:`pv_commissions`

        """

        return self.pv_premiums() - self.pv_claims() - self.pv_expenses() - self.pv_commissions()

    def _f_pv_pols_if(self):
        """Present value of policies in-force

        .. note::
           This cells is not used by default.

        The discounted sum of the number of in-force policies at each month.
        It is used as the annuity factor for calculating :func:`net_premium_pp`.

        """
        return sum(list(self.pols_if(t) for t in range(self.proj_len())) * self.disc_factors()[:self.proj_len()])

    def _f_pv_premiums(self):
        """Present value of premiums

        .. seealso::

            * :func:`premiums`

        """
        return sum(list(self.premiums(t) for t in range(self.proj_len())) * self.disc_factors()[:self.proj_len()])

    def _f_result_cf(self):
        """Result table of cashflows

        .. seealso::

           * :func:`premiums`
           * :func:`claims`
           * :func:`expenses`
           * :func:`commissions`
           * :func:`net_cf`

        """

        t_len = range(self.proj_len())

        data = {
            "Premiums": [self.premiums(t) for t in t_len],
            "Claims": [self.claims(t) for t in t_len],
            "Expenses": [self.expenses(t) for t in t_len],
            "Commissions": [self.commissions(t) for t in t_len],
            "Net Cashflow": [self.net_cf(t) for t in t_len]
        }
        return self.pd.DataFrame.from_dict(data)

    def _f_result_pols(self):
        """Result table of policy decrement

        .. seealso::

           * :func:`pols_if`
           * :func:`pols_maturity`
           * :func:`pols_new_biz`
           * :func:`pols_death`
           * :func:`pols_lapse`

        """

        t_len = range(self.proj_len())

        data = {
            "pols_if": [self.pols_if(t) for t in t_len],
            "pols_maturity": [self.pols_maturity(t) for t in t_len],
            "pols_new_biz": [self.pols_new_biz(t) for t in t_len],
            "pols_death": [self.pols_death(t) for t in t_len],
            "pols_lapse": [self.pols_lapse(t) for t in t_len]
        }

        return self.pd.DataFrame.from_dict(data)

    def _f_result_pv(self):
        """Result table of present value of cashflows

        .. seealso::

           * :func:`pv_premiums`
           * :func:`pv_claims`
           * :func:`pv_expenses`
           * :func:`pv_commissions`
           * :func:`pv_net_cf`

        """

        cols = ["Premiums", "Claims", "Expenses", "Commissions", "Net Cashflow"]
        pvs = [self.pv_premiums(), self.pv_claims(), self.pv_expenses(), self.pv_commissions(), self.pv_net_cf()]

        return self.pd.DataFrame.from_dict(
                data={"PV": pvs},
                columns=cols,
                orient='index')

    def _f_sex(self): 
        """The sex of the selected model point

        .. note::
           This cells is not used by default.

        The element labeled ``sex`` of the Series returned by
        :func:`model_point`.
        """
        return self.model_point()["sex"]

    def _f_sum_assured(self):
        """The sum assured of the selected model point

        The element labeled ``sum_assured`` of the Series returned by
        :func:`model_point`.
        """
        return self.model_point()["sum_assured"]


    def age(self, t):
        if t in self._v_age:
            return self._v_age[t]
        else:
            val = self._f_age(t)
            self._v_age[t] = val
            return val

    def age_at_entry(self):
        if self._has_age_at_entry:
            return self._v_age_at_entry
        else:
            val = self._v_age_at_entry = self._f_age_at_entry()
            self._has_age_at_entry = True
            return val

    def check_pv_net_cf(self):
        if self._has_check_pv_net_cf:
            return self._v_check_pv_net_cf
        else:
            val = self._v_check_pv_net_cf = self._f_check_pv_net_cf()
            self._has_check_pv_net_cf = True
            return val

    def claim_pp(self, t):
        if t in self._v_claim_pp:
            return self._v_claim_pp[t]
        else:
            val = self._f_claim_pp(t)
            self._v_claim_pp[t] = val
            return val

    def claims(self, t):
        if t in self._v_claims:
            return self._v_claims[t]
        else:
            val = self._f_claims(t)
            self._v_claims[t] = val
            return val

    def commissions(self, t):
        if t in self._v_commissions:
            return self._v_commissions[t]
        else:
            val = self._f_commissions(t)
            self._v_commissions[t] = val
            return val

    def disc_factors(self):
        if self._has_disc_factors:
            return self._v_disc_factors
        else:
            val = self._v_disc_factors = self._f_disc_factors()
            self._has_disc_factors = True
            return val

    def disc_rate_mth(self):
        if self._has_disc_rate_mth:
            return self._v_disc_rate_mth
        else:
            val = self._v_disc_rate_mth = self._f_disc_rate_mth()
            self._has_disc_rate_mth = True
            return val

    def duration(self, t):
        if t in self._v_duration:
            return self._v_duration[t]
        else:
            val = self._f_duration(t)
            self._v_duration[t] = val
            return val

    def duration_mth(self, t):
        if t in self._v_duration_mth:
            return self._v_duration_mth[t]
        else:
            val = self._f_duration_mth(t)
            self._v_duration_mth[t] = val
            return val

    def expense_acq(self):
        if self._has_expense_acq:
            return self._v_expense_acq
        else:
            val = self._v_expense_acq = self._f_expense_acq()
            self._has_expense_acq = True
            return val

    def expense_maint(self):
        if self._has_expense_maint:
            return self._v_expense_maint
        else:
            val = self._v_expense_maint = self._f_expense_maint()
            self._has_expense_maint = True
            return val

    def expenses(self, t):
        if t in self._v_expenses:
            return self._v_expenses[t]
        else:
            val = self._f_expenses(t)
            self._v_expenses[t] = val
            return val

    def inflation_factor(self, t):
        if t in self._v_inflation_factor:
            return self._v_inflation_factor[t]
        else:
            val = self._f_inflation_factor(t)
            self._v_inflation_factor[t] = val
            return val

    def inflation_rate(self):
        if self._has_inflation_rate:
            return self._v_inflation_rate
        else:
            val = self._v_inflation_rate = self._f_inflation_rate()
            self._has_inflation_rate = True
            return val

    def lapse_rate(self, t):
        if t in self._v_lapse_rate:
            return self._v_lapse_rate[t]
        else:
            val = self._f_lapse_rate(t)
            self._v_lapse_rate[t] = val
            return val

    def loading_prem(self):
        if self._has_loading_prem:
            return self._v_loading_prem
        else:
            val = self._v_loading_prem = self._f_loading_prem()
            self._has_loading_prem = True
            return val

    def model_point(self):
        if self._has_model_point:
            return self._v_model_point
        else:
            val = self._v_model_point = self._f_model_point()
            self._has_model_point = True
            return val

    def mort_rate(self, t):
        if t in self._v_mort_rate:
            return self._v_mort_rate[t]
        else:
            val = self._f_mort_rate(t)
            self._v_mort_rate[t] = val
            return val

    def mort_rate_mth(self, t):
        if t in self._v_mort_rate_mth:
            return self._v_mort_rate_mth[t]
        else:
            val = self._f_mort_rate_mth(t)
            self._v_mort_rate_mth[t] = val
            return val

    def net_cf(self, t):
        if t in self._v_net_cf:
            return self._v_net_cf[t]
        else:
            val = self._f_net_cf(t)
            self._v_net_cf[t] = val
            return val

    def net_premium_pp(self):
        if self._has_net_premium_pp:
            return self._v_net_premium_pp
        else:
            val = self._v_net_premium_pp = self._f_net_premium_pp()
            self._has_net_premium_pp = True
            return val

    def policy_term(self):
        if self._has_policy_term:
            return self._v_policy_term
        else:
            val = self._v_policy_term = self._f_policy_term()
            self._has_policy_term = True
            return val

    def pols_death(self, t):
        if t in self._v_pols_death:
            return self._v_pols_death[t]
        else:
            val = self._f_pols_death(t)
            self._v_pols_death[t] = val
            return val

    def pols_if(self, t):
        if t in self._v_pols_if:
            return self._v_pols_if[t]
        else:
            val = self._f_pols_if(t)
            self._v_pols_if[t] = val
            return val

    def pols_if_at(self, t, timing):
        if (t, timing) in self._v_pols_if_at:
            return self._v_pols_if_at[(t, timing)]
        else:
            val = self._f_pols_if_at(t, timing)
            self._v_pols_if_at[(t, timing)] = val
            return val

    def pols_if_init(self):
        if self._has_pols_if_init:
            return self._v_pols_if_init
        else:
            val = self._v_pols_if_init = self._f_pols_if_init()
            self._has_pols_if_init = True
            return val

    def pols_lapse(self, t):
        if t in self._v_pols_lapse:
            return self._v_pols_lapse[t]
        else:
            val = self._f_pols_lapse(t)
            self._v_pols_lapse[t] = val
            return val

    def pols_maturity(self, t):
        if t in self._v_pols_maturity:
            return self._v_pols_maturity[t]
        else:
            val = self._f_pols_maturity(t)
            self._v_pols_maturity[t] = val
            return val

    def pols_new_biz(self, t):
        if t in self._v_pols_new_biz:
            return self._v_pols_new_biz[t]
        else:
            val = self._f_pols_new_biz(t)
            self._v_pols_new_biz[t] = val
            return val

    def premium_pp(self):
        if self._has_premium_pp:
            return self._v_premium_pp
        else:
            val = self._v_premium_pp = self._f_premium_pp()
            self._has_premium_pp = True
            return val

    def premiums(self, t):
        if t in self._v_premiums:
            return self._v_premiums[t]
        else:
            val = self._f_premiums(t)
            self._v_premiums[t] = val
            return val

    def proj_len(self):
        if self._has_proj_len:
            return self._v_proj_len
        else:
            val = self._v_proj_len = self._f_proj_len()
            self._has_proj_len = True
            return val

    def pv_claims(self):
        if self._has_pv_claims:
            return self._v_pv_claims
        else:
            val = self._v_pv_claims = self._f_pv_claims()
            self._has_pv_claims = True
            return val

    def pv_commissions(self):
        if self._has_pv_commissions:
            return self._v_pv_commissions
        else:
            val = self._v_pv_commissions = self._f_pv_commissions()
            self._has_pv_commissions = True
            return val

    def pv_expenses(self):
        if self._has_pv_expenses:
            return self._v_pv_expenses
        else:
            val = self._v_pv_expenses = self._f_pv_expenses()
            self._has_pv_expenses = True
            return val

    def pv_net_cf(self):
        if self._has_pv_net_cf:
            return self._v_pv_net_cf
        else:
            val = self._v_pv_net_cf = self._f_pv_net_cf()
            self._has_pv_net_cf = True
            return val

    def pv_pols_if(self):
        if self._has_pv_pols_if:
            return self._v_pv_pols_if
        else:
            val = self._v_pv_pols_if = self._f_pv_pols_if()
            self._has_pv_pols_if = True
            return val

    def pv_premiums(self):
        if self._has_pv_premiums:
            return self._v_pv_premiums
        else:
            val = self._v_pv_premiums = self._f_pv_premiums()
            self._has_pv_premiums = True
            return val

    def result_cf(self):
        if self._has_result_cf:
            return self._v_result_cf
        else:
            val = self._v_result_cf = self._f_result_cf()
            self._has_result_cf = True
            return val

    def result_pols(self):
        if self._has_result_pols:
            return self._v_result_pols
        else:
            val = self._v_result_pols = self._f_result_pols()
            self._has_result_pols = True
            return val

    def result_pv(self):
        if self._has_result_pv:
            return self._v_result_pv
        else:
            val = self._v_result_pv = self._f_result_pv()
            self._has_result_pv = True
            return val

    def sex(self):
        if self._has_sex:
            return self._v_sex
        else:
            val = self._v_sex = self._f_sex()
            self._has_sex = True
            return val

    def sum_assured(self):
        if self._has_sum_assured:
            return self._v_sum_assured
        else:
            val = self._v_sum_assured = self._f_sum_assured()
            self._has_sum_assured = True
            return val



    def _mx_copy_params(self, other):
        # Parameter assignment
        other.point_id = self.point_id

    @staticmethod
    def _mx_assign_params(_mx_space, point_id):
        # Parameter assignment
        _mx_space.point_id = point_id

    def __call__(self, point_id):
        _mx_key = point_id
        if _mx_key in self._mx_itemspaces:
            return self._mx_itemspaces[_mx_key]
        else:
            _mx_base = self
            _mx_root = _mx_base.__class__(self)
            for _mx_s, _mx_b in zip(_mx_root._mx_walk(), _mx_base._mx_walk()):
                _mx_s._mx_copy_refs(_mx_b, _mx_base)
                for _mx_r in self._mx_roots:
                    _mx_r._mx_copy_params(_mx_s)

                self._mx_assign_params(_mx_s, point_id)
                _mx_s._mx_roots.extend(self._mx_roots)
                _mx_s._mx_roots.append(_mx_root)

            self._mx_itemspaces[_mx_key] = _mx_root
            return _mx_root



    def __getitem__(self, item):
        return self.__call__(item)


