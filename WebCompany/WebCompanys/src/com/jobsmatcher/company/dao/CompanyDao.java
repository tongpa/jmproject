package com.jobsmatcher.company.dao;

import java.util.List;
import java.util.Map;

import com.jobsmatcher.company.model.Company; 

public interface CompanyDao extends AbstractDao<Company, String> {
	public boolean saveCompany(Company company);
	public boolean updateCompany(Company company);
	
	
	public List<Company> listCompanyByName(String name,int start,int limit, int page);
	
	public Company getCompanyById(String id);
	public void deleteById(Company company);
	
	 
	
	public List<Map<String, String>> listTotalInDate(String startDate, String stopDate, int start, int limit, int page);
	
	public List<Map<String, String>>  getTotalComnany();
	
	public int getSizeByName(String name);
	
	
	
	
}
