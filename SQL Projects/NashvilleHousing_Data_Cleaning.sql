--Cleaning Data in SQL Queries

select *
from [project portfolio in sql]..NashvilleHousing 


-- standardize Date Format

Select saleDate, CONVERT(Date,SaleDate) as SaleDate
From [project portfolio in sql].dbo.NashvilleHousing

ALTER TABLE NashvilleHousing
Add SaleDateConverted Date;

Update NashvilleHousing
SET SaleDateConverted = CONVERT(Date,SaleDate)




-- Populate Property Address data

Select * 
From [project portfolio in sql].dbo.NashvilleHousing
--where PropertyAddress is null
order by ParcelID

Select X.ParcelID, X.PropertyAddress, y.ParcelID, y.PropertyAddress, ISNULL(X.PropertyAddress, y.PropertyAddress)
From [project portfolio in sql].dbo.NashvilleHousing x
join [project portfolio in sql].dbo.NashvilleHousing y
on X.ParcelID = y.ParcelID
and x.[UniqueID ] <> y.[UniqueID ]
where x.PropertyAddress is null

update x
set PropertyAddress = ISNULL(X.PropertyAddress, y.PropertyAddress)
From [project portfolio in sql].dbo.NashvilleHousing x
join [project portfolio in sql].dbo.NashvilleHousing y
on X.ParcelID = y.ParcelID
and x.[UniqueID ] <> y.[UniqueID ]
where x.PropertyAddress is null


-- Breaking out Address into Individual Columns(Address, City, State)

Select PropertyAddress 
From [project portfolio in sql].dbo.NashvilleHousing
--where PropertyAddress is null
--order by ParcelID

Select 
substring(PropertyAddress, 1, charindex(',', PropertyAddress)-1) as Address	
--,charindex(',', PropertyAddress)  
,substring(PropertyAddress, charindex(',', PropertyAddress)+1, len(PropertyAddress)) as City
From [project portfolio in sql].dbo.NashvilleHousing

ALTER TABLE NashvilleHousing
Add PropertySplitAddress Nvarchar(255);

Update NashvilleHousing
SET PropertySplitAddress = substring(PropertyAddress, 1, charindex(',', PropertyAddress)-1)

ALTER TABLE NashvilleHousing
Add PropertySplitCity Nvarchar(255);

Update NashvilleHousing
SET PropertySplitCity = substring(PropertyAddress, charindex(',', PropertyAddress)+1, len(PropertyAddress)) 

Select PropertyAddress 
From [project portfolio in sql].dbo.NashvilleHousing


-- Another Method of Breaking out Address into Individual Columns(Address, City, State)

Select OwnerAddress
From [project portfolio in sql].dbo.NashvilleHousing

Select 
parsename(replace(OwnerAddress, ',', '.'), 3)
,parsename(replace(OwnerAddress, ',', '.'), 2)
,parsename(replace(OwnerAddress, ',', '.'), 1)
From [project portfolio in sql].dbo.NashvilleHousing

ALTER TABLE NashvilleHousing
Add OwnerSplitAddress Nvarchar(255);

Update NashvilleHousing
SET OwnerSplitAddress = parsename(replace(OwnerAddress, ',', '.'), 3)

ALTER TABLE NashvilleHousing
Add OwnerSplitCity Nvarchar(255);

Update NashvilleHousing
SET OwnerSplitCity = parsename(replace(OwnerAddress, ',', '.'), 2)

ALTER TABLE NashvilleHousing
Add OwnerSplitState Nvarchar(255);

Update NashvilleHousing
SET OwnerSplitState = parsename(replace(OwnerAddress, ',', '.'), 1)


-- Change Y and N to Yes and No in Sold as Vacant field

Select distinct(SoldasVacant), count(SoldasVacant)
From [project portfolio in sql].dbo.NashvilleHousing
group by SoldasVacant
order by 2

select SoldasVacant
,case when SoldasVacant = 'Y' then 'Yes'
when SoldasVacant = 'N' then 'No'
else SoldasVacant
end
From [project portfolio in sql].dbo.NashvilleHousing

update NashvilleHousing
set SoldasVacant = case when SoldasVacant = 'Y' then 'Yes'
	when SoldasVacant = 'N' then 'No'
	else SoldasVacant
	end


-- Remove Duplicates

with RowNumberCTE as(
select *,
	Row_Number() over(
	partition by ParcelID,
				PropertyAddress,
				SalePrice,
				SaleDate,
				LegalReference
				order by
					UniqueID
					) Row_Number

From [project portfolio in sql].dbo.NashvilleHousing
--order by PacelID
)
delete
--select *		-- uncomment this to view the CTE 
from RowNumberCTE
where row_NUmber > 1
--order by PropertyAddress


-- Delete Unused Columns

select *
From [project portfolio in sql].dbo.NashvilleHousing


ALTER TABLE NashvilleHousing
drop column SalePrice



-- Adding '$' to the SalePrice column

Select SalePrice, '$' + CONVERT(nvarchar(50), cast(SalePrice as int)) as SalePrice
From [project portfolio in sql].dbo.NashvilleHousing

ALTER TABLE NashvilleHousing
Add SalePriceinDollar Nvarchar(255);

Update NashvilleHousing
SET SalePriceinDollar = '$' + CONVERT(nvarchar(50), cast(SalePrice as int))

select *
From [project portfolio in sql].dbo.NashvilleHousing
