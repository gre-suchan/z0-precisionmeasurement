P := python
R := Rscript

GROPEDIR = part1/preliminary_hists/
PDIR = part2/hists/
op1h = plot_data/part1/hists/
op2c = plot_data/part2/crosssections/
op2e = plot_data/part2/efficiencies/
op2m = plot_data/part2/mc_hists/
op2afb = plot_data/part2/forward_backward/

.PHONY: all efficiencies

all: $(op1h) $(op2c) $(op2e) $(op2m) $(op2afb)

efficiencies: $(op2e)

grope: $(op1h)

forward_backward_asymmetry: $(op2afb)

crosssections: $(op2c)

hists: $(op2m)

$(op1h) :
	mkdir -p $(@D)
	(cd $(GROPEDIR) && $(R) export.r )

$(op2e):
	mkdir -p $(@D)
	(cd $(PDIR) && $(P) matrix_inversion_export.py )

$(op2m):
	mkdir -p plot_data/part2/mc_hists
	mkdir -p plot_data/part2/opal_hists
	(cd $(PDIR) && $(P) export_hist.py )

$(op2afb):
	mkdir -p $(@D)
	(cd $(PDIR) && $(P) forward_backward.py )

$(op2c):
	mkdir -p $(@D)
	(cd $(PDIR) && $(P) opal_crosssections.py )

clean:
	$(RM) -r -f plot_data/
