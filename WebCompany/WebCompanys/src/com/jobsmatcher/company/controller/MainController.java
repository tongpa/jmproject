package com.jobsmatcher.company.controller;

 

import javax.servlet.http.HttpServletRequest;
 

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.authentication.AnonymousAuthenticationToken;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.authentication.LockedException;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam; 
import org.springframework.web.servlet.ModelAndView;

import com.jobsmatcher.company.dao.CompanyDao; 

import org.apache.log4j.Logger;
@Controller
public class MainController {
	
	final static Logger logger = Logger.getLogger(MainController.class);
	@Autowired
	private CompanyDao companyDao;
	
	
	
	@RequestMapping(value = "/", method = RequestMethod.GET)
	public ModelAndView index() {
		ModelAndView model = new ModelAndView();
		   
		  model.setViewName("company/index");
		  System.out.println("Test Hello");
		  logger.info("Test Hello log");
		  logger.warn("Test Hello log");
		  logger.error("Test Hello log");
		 // model.setViewName("company/sample");
		  //System.out.println("load");
		  return model;
	 
		}
	
	@RequestMapping(value = "/login", method = RequestMethod.GET)
	public ModelAndView login(@RequestParam(value = "error", required = false) String error,
			@RequestParam(value = "logout", required = false) String logout, HttpServletRequest request) {

		ModelAndView model = new ModelAndView();
		if (error != null) {
			model.addObject("error", getErrorMessage(request, "SPRING_SECURITY_LAST_EXCEPTION"));
		}

		if (logout != null) {
			model.addObject("msg", "You've been logged out successfully.");
		}
		model.setViewName("login");

		return model;

	}
	
	// customize the error message
		private String getErrorMessage(HttpServletRequest request, String key) {

			Exception exception = (Exception) request.getSession().getAttribute(key);

			String error = "";
			if (exception instanceof BadCredentialsException) {
				error = "Invalid username and password!";
			} else if (exception instanceof LockedException) {
				error = exception.getMessage();
			} else {
				error = "Invalid username and password!";
			}

			return error;
		}

		// for 403 access denied page
		@RequestMapping(value = "/403", method = RequestMethod.GET)
		public ModelAndView accesssDenied() {

			ModelAndView model = new ModelAndView();

			// check if user is login
			Authentication auth = SecurityContextHolder.getContext().getAuthentication();
			if (!(auth instanceof AnonymousAuthenticationToken)) {
				UserDetails userDetail = (UserDetails) auth.getPrincipal();
				System.out.println(userDetail);

				model.addObject("username", userDetail.getUsername());

			}

			model.setViewName("403");
			return model;

		}
	
}
