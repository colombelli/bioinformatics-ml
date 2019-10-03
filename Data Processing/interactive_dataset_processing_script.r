# varEntryDialog function made by @jbryer
# available in https://gist.github.com/jbryer/3342915

varEntryDialog <- function(vars, 
						   labels = vars,
						   fun = rep(list(as.character), length(vars)),
						   title = 'Variable Entry',
						   prompt = NULL) {
	require(tcltk)
	
	stopifnot(length(vars) == length(labels), length(labels) == length(fun))

	# Create a variable to keep track of the state of the dialog window:
	# done = 0; If the window is active
	# done = 1; If the window has been closed using the OK button
	# done = 2; If the window has been closed using the Cancel button or destroyed
	done <- tclVar(0)

	tt <- tktoplevel()
	tkwm.title(tt, title)	
	entries <- list()
	tclvars <- list()

	# Capture the event "Destroy" (e.g. Alt-F4 in Windows) and when this happens, 
	# assign 2 to done.
	tkbind(tt,"<Destroy>",function() tclvalue(done)<-2)
	
	for(i in seq_along(vars)) {
		tclvars[[i]] <- tclVar("")
		entries[[i]] <- tkentry(tt, textvariable=tclvars[[i]])
	}
	
	doneVal <- as.integer(tclvalue(done))
	results <- list()

	reset <- function() {
		for(i in seq_along(entries)) {
			tclvalue(tclvars[[i]]) <<- ""
		}
	}
	reset.but <- tkbutton(tt, text="Reset", command=reset)
	
	cancel <- function() {
		tclvalue(done) <- 2
	}
	cancel.but <- tkbutton(tt, text='Cancel', command=cancel)
	
	submit <- function() {
		for(i in seq_along(vars)) {
			tryCatch( {
				results[[vars[[i]]]] <<- fun[[i]](tclvalue(tclvars[[i]]))
				tclvalue(done) <- 1
				},
				error = function(e) { tkmessageBox(message=geterrmessage()) },
				finally = { }
			)
		}
	}
	submit.but <- tkbutton(tt, text="Submit", command=submit)
	
	if(!is.null(prompt)) {
		tkgrid(tklabel(tt,text=prompt), columnspan=3, pady=10)
	}
	
	for(i in seq_along(vars)) {
		tkgrid(tklabel(tt, text=labels[i]), entries[[i]], pady=10, padx=10, columnspan=4)
	}
	
	tkgrid(submit.but, cancel.but, reset.but, pady=10, padx=10, columnspan=3)
	tkfocus(tt)

	# Do not proceed with the following code until the variable done is non-zero.
	#   (But other processes can still run, i.e. the system is not frozen.)
	tkwait.variable(done)
	
	if(tclvalue(done) != 1) {
		results <- NULL
	}
	
	tkdestroy(tt)
	return(results)
}



print("Choose file to be processed...")
if (interactive()) {
    fileName <- file.choose()
} else {
    
}



print("Reading dataset...")
df <- read.delim(fileName, header=TRUE)

colValue <- varEntryDialog(vars="Classification label \n(must be integer)")
colValue <- as.integer(colValue)

print("Processing dataset...")

# Transpose df maintaining header
df <- setNames(as.data.frame(t(df[,-1])), df[,1])

# Adding class column
df$class <- colValue

print("Choose file name...")
fileName = file.choose(new = TRUE)

print("Saving processed dataset...")
write.table(df, fileName, sep="\t", row.names = TRUE, col.names = TRUE)

print("Done!")
